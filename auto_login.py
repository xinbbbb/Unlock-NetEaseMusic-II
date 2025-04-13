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
    browser.add_cookie({"name": "MUSIC_U", "value": "008FA74647AAC3B1F2EAEC82BCD5736D97F8CBCA0873CDC7C37663FADDBBE7B9152A9808DFB16C8E0297AD0E7CEF3BA07ABCA2C2316C11E7338B5218CC47612F99297AC66FA06A801A0E84550A18CA63451064C0CDEBA00C08B74FD762C2885C650AFE4B4FF8960CAE87DFF4673CDC2AAAFC809665FD4AF2819D106AEB67F8B3C2508A0317CE91DC159D4943BFF6CC025DDF7633829ED2EE6F9B515D692FDA2EFA6F0D63EE287F864C1733FCF091BC224764BE7DA3F8060A0473C3689B23D520A696F2C895D9A9BA304BCDF3CC1D7A1F0403EE22D9DBBC24E81C24F32C0FCBCE872D03504256E52A868445E9AA7B552266CA6D14C7DC13741B6159CC10ACE3256FBCF5185AB8E5C4893B2B1D79E30B851E6A76E76E1110974D5F731540F46B5A0F4D4492B7546D2CCECC95507A66A29B06E3B64D00EA3B0C6BEC57A81C6D9EC9F3C8DAB311B52D10755FEA2BBE9DD1FE5D8C99AAF28A83E1E82685669163720D7E"})
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
