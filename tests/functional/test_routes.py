from iebank_api import app
import pytest

def test_hello_world(testing_client):
    """Test the '/' route."""
    response = testing_client.get('/')
    assert response.data == b'Hello, World!'


def test_skull(testing_client):
    """Test the '/skull' route."""
    response = testing_client.get('/skull')
    assert response.status_code == 200
    assert b'Database URL:' in response.data


def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200


def test_get_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'country': 'Uruguay', 'currency': '€'})
    account_id = response.get_json()['id']

    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    assert b'John Doe' in response.data
    assert b'Uruguay' in response.data


def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404


def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'country': 'Uruguay', 'currency': '€'})
    assert response.status_code == 200


def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is updated (PUT)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'country': 'Uruguay', 'currency': '€'})
    account_id = response.get_json()['id']

    response = testing_client.put(f'/accounts/{account_id}', json={'name': 'Jane Doe', 'country': 'Brazil'})
    assert response.status_code == 200
    assert b'Jane Doe' in response.data
    assert b'Brazil' in response.data


def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is deleted from (DELETE)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'country': 'Uruguay', 'currency': '€'})
    account_id = response.get_json()['id']

    response = testing_client.delete(f'/accounts/{account_id}')
    assert response.status_code == 200
    assert b'John Doe' in response.data

    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 404