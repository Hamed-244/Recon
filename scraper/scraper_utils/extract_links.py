import requests
import threading
from bs4 import BeautifulSoup

def get_links(url , site_map):
    try:
        response = requests.get( url , timeout=5)

        soup = BeautifulSoup(response.content , 'html.parser')

        # Find all the links on the page
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            # Ignore links that are not URLs or duplicated URLs
            if href is not None and href.startswith("http") and href not in [x for links in site_map for x in site_map[links]]:
                links.append(href)

        return links
    except :
        return []

# main link function
def crawl_site(url, depth ):
    site_map = {}
    def crawl(url, current_depth):
        if current_depth == depth:
            return
            
        try :
            links = get_links(url , site_map)
            site_map[url] = links

            # Crawl each link recursively with multithreading
            links_threading = []

            for link in links:
                if link not in site_map:
                    links_threading.append(threading.Thread(target=crawl , args=(link, current_depth + 1) ) )

            for item in links_threading :
                item.start()

            for item in links_threading :
                item.join()

        except Exception as error:
            print(error)

    crawl(url, 0)

    return site_map