from data.testdata import SENTENCES, KEYWORDS, WITHOUT_DIACRITICS, OUT_OF_SAMPLE

from dotenv import load_dotenv

import requests
import pytest
import os

load_dotenv()
API_KEY = os.getenv("API_KEY_RBA")
BASE_URL = os.getenv("BASE_URL")
HEADERS = {"x-api-key": API_KEY}  # api key is sent in header for auth

intents = set([item["intent"] for item in SENTENCES])
baseline = 1 / len(intents)


def get_confidences_trained():
    confidences_correct = []
    for item in SENTENCES:
        post_request = requests.post(
            f"{BASE_URL}/prompt", headers=HEADERS, json={"message": item["sentence"]}
        )
        if post_request.status_code == 200:
            response_data = post_request.json()
            print(response_data)
            print(item["intent"])
            confidences_correct.append(float(response_data["probs"][item["intent"]]))
    return confidences_correct


# write confidences to csv for analysis
with open("data/confidences_trained.csv", "w") as f:
    f.write("confidence\n")
    for c in get_confidences_trained():
        f.write(f"{c}\n")


def test_confidences_trained():
    confidences_correct = get_confidences_trained()
    for c in confidences_correct:
        assert c > baseline  # assume above baseline confidence for correct predictions
