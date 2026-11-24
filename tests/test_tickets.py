from urllib import response

import requests
import pytest

pytestmark=pytest.mark.api

# BASE_URL = "http://127.0.0.1:8000"
RESPONSE_TIME_HOURS={"P1":4,"P2":24,"P3":72}

@pytest.fixture
def tickets(base_url):
    #print("Fetching tickets from API...")
    response = requests.get(f"{base_url}/tickets")
    return response.json()

def test_health_check_returns_ok(base_url):
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_tickets_returns_200(base_url):
    response = requests.get(f"{base_url}/tickets")
    assert response.status_code == 200

@pytest.mark.parametrize("ticket_id", [1, 2, 3, 4, 5])  
def test_get_one_ticket_returns_200(base_url, ticket_id):
    response = requests.get(f"{base_url}/tickets/{ticket_id }")
    assert response.status_code == 200


def test_get_one_ticket_1_has_correct_data(base_url):
    response = requests.get(f"{base_url}/tickets/1")
    assert response.status_code == 200
    ticket = response.json()
    assert ticket["id"] == 1
    assert ticket["title"] == "Cannot connect to VPN"
    assert ticket["category"] == "IT"
    assert ticket["status"] == "open"


def test_there_are_5_tickets(tickets):
    assert len(tickets)==5

def test_every_ticket_follows_the_rules(tickets):
    for ticket in tickets:
        assert 5<=len(ticket["title"])<=100
        assert ticket["category"] in ["IT","HR"]
        assert ticket["status"] == "open"

@pytest.mark.parametrize("category,expected_count", [("IT", 3), ("HR", 2)])
def test_filter_tickets_by_category(category,expected_count,base_url):
    response = requests.get(f"{base_url}/tickets",params={"category":category})
    tickets=response.json()
    assert len(tickets)==expected_count
    for ticket in tickets:
        assert ticket["category"]==category


@pytest.mark.parametrize("ticket_id", [0,999,-1])

def test_missing_ticket_returns_404(ticket_id,base_url):
    response = requests.get(f"{base_url}/tickets/{ticket_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"

def test_ticket_response_time_matches_priority(tickets):
    for ticket in tickets:
        assert ticket["response_time_hours"] == RESPONSE_TIME_HOURS[ticket["priority"]]

@pytest.mark.skip(reason="This test is not implemented yet")
def test_close_ticket(base_url,new_ticket):
    response=requests.post(f"{base_url}/tickets/{new_ticket['id']}/close")
    assert response.status_code==200

@pytest.mark.parametrize("length,expected_status", [(4, 422), (5, 201), pytest.param(100, 201,marks=pytest.mark.xfail(reason="Bug: a 100 character title is rejected")), (101, 422)])
def test_title_length_boundaries(base_url,length,expected_status):
    ticket = {"title": "x" * length, "category": "IT"}
    response = requests.post(f"{base_url}/tickets", json=ticket)
    assert response.status_code == expected_status

    