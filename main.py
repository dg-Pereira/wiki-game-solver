import requests
from bs4 import BeautifulSoup

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
#RANDOM_URL = "https://en.wikipedia.org/wiki/Pio_(surname)"

def get_url_links(url, write_to_file = False):
    def clean_filter(a):
        if a['href'].startswith("/wiki/") and \
            not a['href'][6:].startswith(("Main_Page", "Talk:", "Category:", "Template:", "Template_talk:", "Special:", "Help:", "File:", "Portal:", "Wikipedia:")):
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
    links = filter(clean_filter, links)

    return links


print("Links:")

links = get_url_links(RANDOM_URL, write_to_file=True)

for l in links:
    print(l['href'])