from data.testdata import SENTENCES, KEYWORDS, WITHOUT_DIACRITICS, OUT_OF_SAMPLE

from selenium import webdriver
from selenium.webdriver.common.by import By

from dotenv import load_dotenv

import os
import pytest


load_dotenv()
API_KEY = os.getenv("API_KEY_RBA")
BASE_URL = os.getenv("BASE_URL")


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
    msg_elements = driver.find_elements(
        By.XPATH, "//div[@class='msg' and .//div[@class='bot']]//div[@class='meta']"
    )
    if msg_elements:
        last_msg = msg_elements[-1]
        intent = last_msg.text.split("|")[0].strip().split(":")[1].strip()
        confidence = last_msg.text.split("|")[1].strip().split(":")[1].strip()
        return intent, confidence
    else:
        return "", 0


def write_api_key(driver, api_key):
    api_key_input = driver.find_element(By.ID, "api-key-input")
    api_key_input.send_keys(api_key)

    save_key_button = driver.find_element(By.ID, "save-key-btn")
    save_key_button.click()


# Test to see if the server is up by checking the health endpoint
def test_health(driver):
    driver.get("http://localhost:8000/health")
    assert '{"status":"ok"}' in driver.page_source


# Test exact same training sentences, I won't be collecting failures here
def test_train_sentences(driver):
    driver.get("http://localhost:8000")

    write_api_key(driver, API_KEY)

    chat_input = driver.find_element(By.ID, "chat-input")
    send_button = driver.find_element(By.ID, "chat-send")

    for item in SENTENCES:
        chat_input.send_keys(item["sentence"])
        send_button.click()

        chat_input.clear()
        intent, _ = get_last_bot_data(driver)
        assert intent == item["intent"]


# Test keywords obvious for each intent, collect failures and print them at the end
def test_keywords(driver):
    driver.get("http://localhost:8000")

    write_api_key(driver, API_KEY)

    chat_input = driver.find_element(By.ID, "chat-input")
    send_button = driver.find_element(By.ID, "chat-send")

    failures = []

    for item in KEYWORDS:
        expected_intent = item["intent"]
        for kw in item["keywords"]:
            chat_input.send_keys(kw)
            send_button.click()

            chat_input.clear()
            intent, _ = get_last_bot_data(driver)
            try:
                assert intent == expected_intent
            except AssertionError:
                failures.append((kw, expected_intent, intent))

    if failures:
        for fail in failures:
            print(f"Keyword: '{fail[0]}' | Expected: '{fail[1]}' | Got: '{fail[2]}'")
        pytest.fail(f"{len(failures)} keyword tests failed")


# Test keywords without diacritics, since all training sentences have diacritics, expected failures
def test_without_diacritics(driver):
    driver.get("http://localhost:8000")

    write_api_key(driver, API_KEY)

    chat_input = driver.find_element(By.ID, "chat-input")
    send_button = driver.find_element(By.ID, "chat-send")

    failures = []

    for item in WITHOUT_DIACRITICS:
        keyword = item["keyword"]
        expected_intent = item["intent"]

        chat_input.send_keys(keyword)
        send_button.click()

        chat_input.clear()
        intent, _ = get_last_bot_data(driver)
        try:
            assert intent == expected_intent
        except AssertionError:
            failures.append((keyword, expected_intent, intent))

    if failures:
        for fail in failures:
            print(f"Keyword: '{fail[0]}' | Expected: '{fail[1]}' | Got: '{fail[2]}'")
        pytest.fail(f"{len(failures)} without diacritics tests failed")


# Test sentences outside of training set, expected failures
def test_out_of_sample(driver):
    driver.get("http://localhost:8000")

    write_api_key(driver, API_KEY)

    chat_input = driver.find_element(By.ID, "chat-input")
    send_button = driver.find_element(By.ID, "chat-send")

    failures = []

    for item in OUT_OF_SAMPLE:
        sentence = item["sentence"]
        expected_intent = item["intent"]

        chat_input.send_keys(sentence)
        send_button.click()

        chat_input.clear()
        intent, _ = get_last_bot_data(driver)
        try:
            assert intent == expected_intent
        except AssertionError:
            failures.append((sentence, expected_intent, intent))

    if failures:
        for fail in failures:
            print(f"Sentence: '{fail[0]}' | Expected: '{fail[1]}' | Got: '{fail[2]}'")
        pytest.fail(f"{len(failures)} out of sample tests failed")
