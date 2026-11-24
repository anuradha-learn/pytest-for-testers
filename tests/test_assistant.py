import json
from pathlib import Path

import pytest
import requests
# BASE_URL = "http://127.0.0.1:8000"

DATA_FILE= Path(__file__).parent / "data" / "assistant_questions.json"

with open(DATA_FILE) as file:  
    QUESTIONS = json.load(file)

@pytest.mark.ai
@pytest.mark.parametrize("case", QUESTIONS,ids=[case["name"] for case in QUESTIONS])
def test_assistant_answer_has_right_facts(case,base_url):
    response = requests.post(f"{base_url}/assistant/ask", json={"question": case["question"]})
    assert response.status_code == 200
    answer = response.json()
    assert answer["topic"] == case["topic"]
    for fact in case["facts"]:
        assert fact in answer["answer"]