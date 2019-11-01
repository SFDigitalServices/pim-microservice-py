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
    parcel = '1279021'
    response = client.simulate_get('/records/'+parcel, params={'fields':'year_built'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['year_built']

def test_record_building_area(client):
    """ Test record building_area field
    """
    response = client.simulate_get('/records/3512008', params={'fields':'building_area'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert 'building_area' in content['data']

def test_record_ceqacode(client):
    """ Test record ceqacode field
    """
    response = client.simulate_get('/records/1279021', params={'fields':'ceqacode'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['ceqacode']


def test_record_article_11(client):
    """ Test record article_11 field
    """
    response = client.simulate_get('/records/0350004', params={'fields':'article_11'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert content['data']['article_11']

def test_record_combo(client):
    """ Test record retrieval for multiple fields """
    response = client.simulate_get(
        '/records/3512008',
        params={'fields':'year_built,building_area,ceqacode'}
        )
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert 'year_built' in content['data']
    assert 'building_area' in content['data']
    assert 'ceqacode' in content['data']

def test_record_empty(client):
    """ Test empty record
    """
    response = client.simulate_get('/records/123', params={'fields':'year_built'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert 'year_built' in content['data']
    assert not content['data']['year_built']

def test_record_parcels(client):
    """ Test record parcels
    """
    response = client.simulate_get(
                '/records/3512008',
                params={'fields':'building_area,blklot,address'})
    assert response.status_code == 200

    content = json.loads(response.content)
    assert jsend.is_success(content)
    assert 'parcels' in content['data']
    assert isinstance(content['data']['parcels'], list)
    assert content['data']['parcels'][0]['attributes']['blklot'] == '3512008'
    assert 'ADDRESS' not in content['data']['parcels'][0]['attributes']
    assert 'address' in content['data']['parcels'][0]['attributes']
