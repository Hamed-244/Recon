from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from scraper.serializers import ReconSiteSerializer
from .utils import get_domain
import threading

from .scraper_utils import subdomains, extract_files, extract_links, extract_Technologies, open_ports, screenshoot, server_info 

from queue import Queue

def get_data(url, domain, data):
    # Create a queue to store the results from the threads
    result_queue = Queue()

    # Define functions to capture the results from the threads
    def capture_result(func, key, args):
        try:

            result = func(*args)
            result_queue.put((key, result))
        except Exception as error :
            print(error ,'key :', key)

    # Define the thread targets and arguments
    thread_targets = [
        (extract_files.extract_files, 'Files', [url]),
        (extract_links.crawl_site, 'Links', [url, 2]),
        (subdomains.subdomain_check, 'Subdomains', [domain]),
        (open_ports.port_scanner, 'Ports', [domain]),
        (server_info.get_url_info, 'Informations', [domain]),
        (screenshoot.capture_screenshot, 'Screenshot', [url, domain]),
        (extract_Technologies.wappalyzer, 'Technologies', [url])
    ]

    threads = []
    # Create and start the threads
    for target, key, args in thread_targets:
        thread = threading.Thread(target=capture_result, args=(target, key, args))
        threads.append(thread)
        thread.start()

    # Join the threads and capture the results
    for thread in threads:
        thread.join()

    # Store the results in the data dictionary
    while not result_queue.empty():
        key, result = result_queue.get()
        data[key] = result

    return data

class ReconSiteView (APIView):
    def post(self , request):
        serializer = ReconSiteSerializer(data=request.data)
        if serializer.is_valid():
            url =serializer.data.get('url')
            # check cached data
            if cache.get(url) :
                response_data = cache.get(url)
            else :
                domain = get_domain(url)
                response_data = {'url' : url , 'domain' : domain}
                # add data to response
                get_data(url=url , domain=domain ,data = response_data)
                cache.set(url, response_data, 1800)

            return Response(response_data, status=200)
        return Response(serializer.errors , status=403)
