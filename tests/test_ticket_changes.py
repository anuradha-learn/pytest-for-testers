import pytest
import requests

pytestmark=pytest.mark.api

NEW_TICKET={
    "title": "Printer not working",
    "category": "IT",
    "priority": "P1"}

@pytest.fixture
def new_ticket(base_url):
    print("Creating a new ticket for test...")
    response = requests.post(f"{base_url}/tickets", json=NEW_TICKET)
    ticket= response.json()
    yield ticket
    print("Deleting the new ticket after test...")
    requests.delete(f"{base_url}/tickets/{ticket['id']}")


def test_delete_ticket(base_url,new_ticket):
    response = requests.delete(f"{base_url}/tickets/{new_ticket['id']}")
    assert response.status_code == 204
    response = requests.get(f"{base_url}/tickets/{new_ticket['id']}")
    assert response.status_code == 404

def test_create_ticket_returns_201(base_url):
   response = requests.post(f"{base_url}/tickets", json=NEW_TICKET)

   assert response.status_code == 201
   ticket = response.json()
   assert ticket["title"] == "Printer not working"
   assert ticket["status"] == "open"
   assert ticket["response_time_hours"] == 4

def test_priority_defaults_to_p3(base_url):
    response = requests.post(f"{base_url}/tickets", json={"title": "Mouse not working", "category": "IT"})
    assert response.status_code == 201
    ticket = response.json()
    assert ticket["priority"] == "P3"
    assert ticket["response_time_hours"] == 72

def test_new_ticket_can_be_fetched(new_ticket,base_url):
    response = requests.get(f"{base_url}/tickets/{new_ticket['id']}")
    assert response.status_code == 200
    ticket = response.json()
    assert ticket["title"] == "Printer not working"


