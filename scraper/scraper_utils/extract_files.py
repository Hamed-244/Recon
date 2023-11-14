import requests
from bs4 import BeautifulSoup 
from urllib.parse import urljoin

def find_list_resources (tag , attribute , soup , absolute_url = False , url = None):
   tag_list = []
   for x in soup.findAll(tag):
       try:
            tag = x[attribute]
            if absolute_url:
                tag = urljoin(base=url , url=tag)
            if tag not in tag_list :
                tag_list.append(tag)
       except KeyError:
           pass
   return(tag_list)


def extract_files(url):
    try :
        request_data = requests.get(url=url)
        if request_data.status_code == 200 :
            soup = BeautifulSoup(request_data.content , features="lxml")

            image_scr = find_list_resources('img',"src", soup , absolute_url=True)   
            script_src = find_list_resources('script',"src", soup , absolute_url=True)    
            linked_files = find_list_resources("link","href", soup , absolute_url=True)
            video_src = find_list_resources("video","src", soup , absolute_url=True)         
            audio_src = find_list_resources("audio","src", soup , absolute_url=True) 
            iframe_src = find_list_resources("iframe","src", soup , absolute_url=True)
            embed_src = find_list_resources("embed","src", soup , absolute_url=True)
            object_data = find_list_resources("object","data", soup , absolute_url=False)         
            soruce_src = find_list_resources("source","src", soup , absolute_url=True)
            files = {'image' : image_scr , 'script':script_src , 'link' : linked_files , 'video' :video_src , 'audio' : audio_src , 'iframe' : iframe_src , 'embed' : embed_src , 'object' : object_data , 'sourse' : soruce_src}
            return files
        return None
    except :
        return None