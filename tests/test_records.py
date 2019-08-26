# pylint: disable=redefined-outer-name
"""Tests for Records resource"""
import json
import pytest
import jsend
import falcon
import service.microservice

@pytest.fixture()
def client():
    """ client fixture """
    return falcon.testing.TestClient(service.microservice.start_service())

def test_records_index_default(client):
    """Test records index (default state) """
    response = client.simulate_get('/records/')
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert content['data']['message'] == falcon.HTTP_200

def test_record_year_built(client):
    """ Test record year_built field
    """
    response = client.simulate_get('/records/3512008', params={'fields':'year_built'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['parcel'] == '3512008'
    assert 'year_built' in content['data']

def test_record_building_area(client):
    """ Test record building_area field
    """
    response = client.simulate_get('/records/3512008', params={'fields':'building_area'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['parcel'] == '3512008'
    assert 'building_area' in content['data']

def test_record_combo(client):
    """ Test record retrieval for multiple fields """
    response = client.simulate_get('/records/3512008', params={'fields':'year_built,building_area'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['parcel'] == '3512008'
    assert 'year_built' in content['data']
    assert 'building_area' in content['data']

def test_record_empty(client):
    """ Test empty record
    """
    response = client.simulate_get('/records/123', params={'fields':'year_built'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['parcel'] == '123'
    assert 'year_built' not in content['data']
