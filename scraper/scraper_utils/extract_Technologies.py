from Wappalyzer import Wappalyzer, WebPage
import warnings
def wappalyzer (url) :
    try :
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wappalyzer = Wappalyzer.latest()
            webpage = WebPage.new_from_url(url)
            info = wappalyzer.analyze_with_versions_and_categories(webpage)
            return  info
    except Exception as error :
        print('error in wapplayzer' , error)
        return []