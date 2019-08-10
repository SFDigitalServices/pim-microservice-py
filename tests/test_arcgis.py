# pylint: disable=redefined-outer-name
"""Tests for ArcGIS resource"""
import json
import pytest
import jsend
from falcon import testing
import service.microservice
from service.resources.arcgis import Arcgis

@pytest.fixture()
def client():
    """ client fixture """
    return testing.TestClient(service.microservice.start_service())

def test_arcgis_welcome(client):
    """Test arcgis welcome"""
    response = client.simulate_get('/arcgis/welcome')
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)

def test_arcgis_parcels_default(client):
    """Test arcgis parcels
        default state
    """
    response = client.simulate_get('/arcgis/parcels')
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert content['data']['message'] == 'parcels'

def test_arcgis_parcels_empty(client):
    """Test arcgis parcels
        empty state
    """
    response = client.simulate_get('/arcgis/parcels', params={'address':'1234'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert content['data']['parcels'] == {}

def test_arcgis_parcels_basic(client):
    """Test arcgis parcels
        basic state
    """
    response = client.simulate_get('/arcgis/parcels', params={'address':'1650 mission street'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert len(content['data']['parcels']) == 1
    assert content['data']['parcels'][0]['attributes']['blklot'] == '3512008'
    assert content['data']['parcels'][0]['attributes']['ADDRESS'] == '1650 MISSION ST'
    assert 'geometry' not in content['data']['parcels'][0]

def test_arcgis_parcels_basic_geometry(client):
    """Test arcgis parcels
        basic with geometry state
    """
    response = client.simulate_get(
        '/arcgis/parcels',
        params={'address':'1650 mission street', 'returnGeometry':'true'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert len(content['data']['parcels']) == 1
    assert content['data']['parcels'][0]['attributes']['blklot'] == '3512008'
    assert content['data']['parcels'][0]['attributes']['ADDRESS'] == '1650 MISSION ST'
    assert isinstance(content['data']['parcels'][0]['geometry']['rings'], list)

def test_arcgis_parcels_basic_suggestion(client):
    """Test arcgis parcels
        basic with suggestion state
    """
    response = client.simulate_get(
                '/arcgis/parcels',
                params={'address':'1650 mission street suite 400', 'returnSuggestions':'true'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert len(content['data']['parcels']) == 1
    assert content['data']['parcels'][0]['attributes']['blklot'] == '3512008'
    assert content['data']['parcels'][0]['attributes']['ADDRESS'] == '1650 MISSION ST'

def test_arcgis_parcels_basic_no_suggestion(client):
    """Test arcgis parcels
        basic with no suggestion state
    """
    response = client.simulate_get(
                '/arcgis/parcels',
                params={'address':'1650 mission street suite 1000'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert not content['data']['parcels']

def test_arcgis_parcels_suggest_range(client):
    """Test arcgis parcels
        range suggestion state
    """
    response = client.simulate_get(
                '/arcgis/parcels',
                params={'address':'1651 mission street suite 1000', 'returnSuggestions':'true'})
    assert response.status_code == 200

    content = json.loads(response.content)

    assert jsend.is_success(content)
    assert len(content['data']['parcels']) > 1
    for parcel in content['data']['parcels']:
        assert parcel['attributes']['blklot']
        assert parcel['attributes']['ADDRESS']

def test_query_error():
    """ Test query error state """
    arcgis = Arcgis()
    response = arcgis.query('', {})
    assert response is None

def test_missing_env(client, monkeypatch):
    """ Test missing env variable(s) """
    monkeypatch.setenv('PLN_ARCGIS_PARCEL', '')
    response = client.simulate_get('/arcgis/parcels')
    assert response.status_code is not 200

    content = json.loads(response.content)
    assert jsend.is_error(content)
    assert 'PLN_ARCGIS_PARCEL' in content['message']

def test_parcel_route(client):
    """ Test parcel route"""
    response1 = client.simulate_get('/arcgis/parcels', params={'address':'1650 mission street'})
    assert response1.status_code == 200

    response2 = client.simulate_get('/parcels', params={'address':'1650 mission street'})
    assert response2.status_code == response1.status_code

    assert response2.content == response1.content
