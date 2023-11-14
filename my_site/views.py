from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def Home(request) :
    return render(request , 'home/index.html')