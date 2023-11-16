from django.db import models


class Screenshoot(models.Model) :
    url = models.CharField(max_length=512)
    domain = models.CharField(max_length=128)
    screenshoot = models.ImageField(verbose_name='Screenshoot' , default = 'screenshoots/default.png' , upload_to='screenshoots/')
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.domain