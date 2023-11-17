from django.contrib import admin
from scraper.models import Screenshoot

class ScreenshootAdmin(admin.ModelAdmin) :
    list_filter = ['domain' , 'created']

admin.site.register(Screenshoot , ScreenshootAdmin)