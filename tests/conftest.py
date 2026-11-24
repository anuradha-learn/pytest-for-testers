import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    #print("\nUsing base URL: http://127.0.0.1:8000")
    return "http://127.0.0.1:8000"

@pytest.fixture(autouse=True)
def reset_data(base_url):
    requests.post(f"{base_url}/reset")