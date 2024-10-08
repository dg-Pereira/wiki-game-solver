import requests
from bs4 import BeautifulSoup

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
PHILOSOPHY_URL = "https://www.wikipedia.org/wiki/Philosophy"
#RANDOM_URL = "https://en.wikipedia.org/wiki/Sound"

def get_url_links(url, write_to_file = False):
    def clean_filter(a):
        if a.find_parent('table', class_='infobox'): #if there is an ancestor (recursively) that is a table with the infobox class
            return False
        elif a.find_parent('div', role='note'):
            return False
        elif a.find_parent('figcaption'):
            return False
        elif a.find_parent('table', class_="sidebar"):
            return False
        elif a.find_parent('div', class_="description"):
            return False
        
        if (not url.endswith(a['href']) and # prevent loops by not going to current page
            a['href'].startswith("/wiki/") and #only get links to other wikipedua pages
            not a['href'][6:].startswith(("Main_Page", "Talk:", "Category:", "Template:", "Template_talk:", "Special:", "Help:", "File:", "Portal:", "Wikipedia:"))):
                return True
        else:
            return False
    
    r = requests.get(url)
    json_content = r.content.decode('utf8').replace("'", '"')

    if write_to_file:
         with open("request-content.html", "w") as f:
            f.write(json_content)

    soup = BeautifulSoup(json_content, 'html.parser')

    links = soup.find_all("a", href = True)
    links = list(filter(clean_filter, links))

    return links

def get_first_good_a(_as):
    for a in _as:
        classes = a.parent.get("class")
        if classes == None:
             classes = []
        if "infobox-caption" in classes:
             continue
        return a
    return None

def get_philosophy_chain(start_url=RANDOM_URL):
    found = False
    curr_url = start_url
    chain = []

    while not found:
        chain.append(curr_url)

        if curr_url == PHILOSOPHY_URL:
            found = True
            break

        first_a = get_first_good_a(get_url_links(curr_url, write_to_file=len(chain)==1))
        with open("parent.txt", "a") as f:
            f.write(str(first_a.parent))
            f.write("\n-------\n")
    
        curr_url = "https://www.wikipedia.org" + first_a['href']

        if curr_url in chain:
            break
    return found, chain

print(get_philosophy_chain())