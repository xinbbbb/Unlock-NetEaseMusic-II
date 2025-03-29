# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00229B884011EFFEF5594E76344F75B79288723D9EEA0B3669196C529469B74CD6D083B069BEA65FE9834658D7F68440D9450FDF15359822EBC03332CB12C22EF2D00785B8FF714FCB35D1BAC18B203478B02E7BD2F5F92964EF3EE9DEB1A82B7EF550A4202DD94E37BA9E2C955A777FF422E853A847C4ADFF8634E8B12BFEB61E1B1EF13ECBF1EE1FE9E8D76849F95CBC5EE2AC2C861154BCB7B405873090D3865D3B8B57F81ABD255069510CCB3FDD57DFDC81EFBE89B1D33C50F5818CAC41CB3FDD1ABF5D154189FFD8BB0B8CE51A8441994C63C6AE1F51AD23F3E93A5BBF1F912E052370C1605007702E429E28FE72F8BAB20984461358A67C281FB847021E3CB1A7ABCEC7439FE8383B66E211F918F9760BA88EDB67DCC576ED685863993EBFC6AEC93F689046676348C66DC312E5BFB93EC6F0A663FBEE22664AD6DBBBB5A0DBE258FAA6F3F3189341C4AA56D9D254DC7DCE89CE09955173170745956D94"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
