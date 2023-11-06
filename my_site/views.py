from django.shortcuts import render

def Home(request) :
    return render(request , 'home/index.html')