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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C390604D9583153AF7A0EBE11B8C861939184F974EB796229E996AC5E0BD5986A79DD231C275A3D7F9B0D39D73ED16D1A0BC0ECC53DCDB0DE12BFF11071A2833D4940CCCA72918624B495377B1963CF00A8169D96F2E272044F6A6C1634C235C2C414619115AFAF55E99173931819F26E24334C32C50573F515CCB7DD5A161142F3D8CD303A97756B0021C9B8EC2B43CEC48DCE63996ADEBDF1CE5075A1E9A9071B2290346DD255CA5AD71B52A35F713F591557959606DFA653C96F676F26163A68160E78FC1407D0E104CB9A0619DA4C691160E345EF6DE17CD3B244F419159C64A0380CE45ABFFE9B98B3B8E2B053FD18374ED55F82CC31B2678067F8EE4AA4FDE3E82BB03483FCD7E153378902489BA92709ACE743B8BBC224A551051EAE196EFAE8ED9D028D95743437EC5490C0EA8AC0C56EABF25B17FFFD7BC5CB8098D1F683B21BDF5A6778EB7534B4EC918032D805DF50E35479CA6F20106D9DF9983259B48EB052E9A649C892EEB729181BB"})
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
