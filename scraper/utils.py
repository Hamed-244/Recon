from urllib.parse import urlparse

def get_domain(url) :
    try:
        domain = urlparse(url).netloc
        domain = '.'.join(domain.split('.')[-2:])
        return domain
    except Exception as error:
        print('error in get domain :' , error)
        return None
        