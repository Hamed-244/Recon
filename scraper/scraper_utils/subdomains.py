import requests
import dns.resolver
import socket
import re
import threading
from bs4 import BeautifulSoup

# get_title
def get_title (html_content) :
    try :
        soup = BeautifulSoup(html_content, 'html.parser')
        title = str(soup.title.string )
        return title
    except Exception as error:
        print('sub domain title error :' ,error)
        return "Unknown"

# get phone number
def get_phonNumber (html_content):
    try :
        phonNumber_regex = r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}"
        phonNumbers = re.findall(phonNumber_regex , html_content)
        return phonNumbers
    except Exception as error:
        print('extract phone number error' , error)
        return []

# get emails
def get_email (html_content) :
    try :
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_regex , html_content)
        return emails
    except Exception as error:
        print('extract email error' ,error)
        return []


# collect title and status code
def subdomain_information (domain) :
    try :
        url = f'http://{domain}'
        request = requests.get(url)
        status_code = request.status_code or 'Unknown'
        html_content = request.content.decode()
        emails = get_email(html_content)
        phonNumbers = get_phonNumber(html_content)
        title = get_title(html_content).strip()
        return {"status" : status_code , "title" : title , "emails" : emails , "phon numbers" : phonNumbers }
    except Exception as error:
        print('get subdomain information error' ,error)
        return {"status" : "Unknown" , "title" : "Unknown" , "emails" : [] , "phon numbers" : []}

def check_subdomain_exists(subdomain , domain, existed_subdomains) :
    sub_name = None
    try :
        answers = dns.resolver.resolve(subdomain + "." + domain , "A")
        for ip in answers:
            sub_name = subdomain + "." + domain
            if sub_name not in existed_subdomains :
                existed_subdomains.append(sub_name)
    except Exception as error :
        pass

def get_subdomain (domain) :
    existed_subdomains = []
    with open ("static/scraper/domainList.txt" , 'r') as wordlist :
        wordlist = wordlist.readlines()
        count = 0
        while count < len(wordlist)-1 :
            threads_list = []
            max_index = count+50 if count +50 < len(wordlist) else len(wordlist)

            for line_index in range(count , max_index):
                line = wordlist[line_index]
                subdomain = line.strip()
                threads_list.append(threading.Thread(target=check_subdomain_exists , args=[subdomain , domain , existed_subdomains]))
                count += 1

            for item in threads_list :
                item.start()

            for item in threads_list :
                item.join()

        return existed_subdomains

# main subdomain check
def subdomain_check(domain):
    try:

        subdomain_info = []
        subdomains = get_subdomain(domain)

        for subname in subdomains :
            ipAddres = socket.gethostbyname(subname)
            more_info = subdomain_information (subname)
            subdomain_info.append({"subName" : subname , "ip" : ipAddres , "status" : more_info["status"] , "title" : more_info["title"] , "emails" : more_info["emails"] ,"phonNumbers" : more_info["phon numbers"] })
        
        return subdomain_info
    except Exception as error :
        print('error in subdomain check' , error)
        return None