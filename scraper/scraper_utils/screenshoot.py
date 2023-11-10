from django.conf import settings
from selenium import webdriver
import os
import time

def capture_screenshot(url , domain ):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)

        # Open the provided URL
        driver.get(url)
        time.sleep(3)
        # Create the screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(settings.MEDIA_ROOT, 'screenshoots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        # Capture a screenshot
        screenshot_path = os.path.join(screenshots_dir, f'{domain}.png')
        driver.save_screenshot(screenshot_path)

        # Clean up
        driver.quit()
        
        # Return the URL of the screenshot
        return screenshot_path
    except Exception as error:
        # Handle any exceptions
        print('error in capture screenshoot' , error)
        default_screenshoot_dir = os.path.join(settings.MEDIA_ROOT, 'screenshoots/default.png')
        return default_screenshoot_dir