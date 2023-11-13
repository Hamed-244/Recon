import os
import time
from selenium import webdriver
from django.conf import settings

def capture_screenshot(url, domain):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # wait until images load
        time.sleep(1)

        # Create the screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(settings.MEDIA_ROOT, 'screenshoots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        # Capture a screenshot
        screenshot_path = os.path.join(screenshots_dir, f'{domain}.png')
        driver.save_screenshot(screenshot_path)

        driver.quit()

        return screenshot_path
    except Exception as error:
        print('error in capture screenshot', error)
        default_screenshot_dir = os.path.join(settings.MEDIA_ROOT, 'screenshoots\\default.png')
        return default_screenshot_dir
