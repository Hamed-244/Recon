import os
import time
from selenium import webdriver
from django.core.files.base import ContentFile
from scraper.models import Screenshoot
import chromedriver_binary

def capture_screenshot(url, domain):
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # wait until images load
        time.sleep(1)

        # Capture a screenshot
        screenshot_filename = f'{domain}.png'
        screenshot_content = driver.get_screenshot_as_png()

        # Create Screenshoot object and save it
        screenshot_obj = Screenshoot(
            url=url,
            domain=domain,
        )
        screenshot_obj.screenshoot.save(screenshot_filename, ContentFile(screenshot_content), save=True)

        driver.quit()

        # Get the URL for the saved screenshot
        screenshot_url = screenshot_obj.screenshoot.url

        return screenshot_url
    except Exception as error:
        print('error in capture screenshot', error)
        default_screenshot_url = '/media/screenshoots/default.png'
        return default_screenshot_url
