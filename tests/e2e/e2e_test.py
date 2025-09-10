from train_sentences import SENTENCES

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

import os
import pytest
import time


load_dotenv()
API_KEY = os.getenv("API_KEY_RBA")

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# IPAK NE TREBA CIJELA PORUKA, samo intent
# def get_last_bot_response(driver):
#     bot_elements = driver.find_elements(By.XPATH, "//div[@class='msg']//div[@class='bot']")
#     if bot_elements:
#         last_response = bot_elements[-1]
#         return last_response.text
#     else:
#         return ""

def get_last_bot_data(driver):
    # msg elements that contain bot div, since intent is outside of bot div
    msg_elements =  driver.find_elements(By.XPATH, "//div[@class='msg' and .//div[@class='bot']]//div[@class='meta']")
    if msg_elements:
        last_msg = msg_elements[-1]
        intent = last_msg.text.split("|")[0].strip().split(":")[1].strip()
        confidence = last_msg.text.split("|")[1].strip().split(":")[1].strip()
        return intent, confidence
    else:
        return "", 0


# Test to see if the server is up by checking the health endpoint
def test_health(driver):
    driver.get("http://localhost:8000/health")
    assert '{"status":"ok"}' in driver.page_source


def test_train_sentences(driver):
    driver.get("http://localhost:8000")

    api_key_input = driver.find_element(By.ID, "api-key-input")
    api_key_input.send_keys(API_KEY)

    save_key_button = driver.find_element(By.ID, "save-key-btn") 
    save_key_button.click()

    chat_input = driver.find_element(By.ID, "chat-input")
    send_button = driver.find_element(By.ID, "chat-send")

    for item in SENTENCES:
        chat_input.send_keys(item["sentence"])
        send_button.click()

        chat_input.clear()
        intent,_ = get_last_bot_data(driver)
        assert intent == item["intent"]