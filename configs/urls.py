from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static 
from django.conf import settings
from scraper.views import ReconSiteView

# local 
from my_site.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home , name="home"),
    path('api/v1/get-site-data/' , ReconSiteView.as_view()),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT )