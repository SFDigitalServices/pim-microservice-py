"""Tests for Records resource"""
import json
from unittest.mock import patch
from service.models.datasf import DataSF

# pylint: disable=line-too-long
MOCK_DATASF_JSON = """[{"title":"180","release_year":"2011","locations":"Epic Roasthouse (399 Embarcadero)","production_company":"SPI Cinemas","director":"Jayendra","writer":"Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ","actor_1":"Siddarth","actor_2":"Nithya Menon","actor_3":"Priya Anand"},{"title":"180","release_year":"2011","locations":"Mason & California Streets (Nob Hill)","production_company":"SPI Cinemas","director":"Jayendra","writer":"Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ","actor_1":"Siddarth","actor_2":"Nithya Menon","actor_3":"Priya Anand"},{"title":"180","release_year":"2011","locations":"Justin Herman Plaza","production_company":"SPI Cinemas","director":"Jayendra","writer":"Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ","actor_1":"Siddarth","actor_2":"Nithya Menon","actor_3":"Priya Anand"}]"""

def test_datasf_filter():
    """ Test DataSF filter with mock response """
    datasf = DataSF()
    with patch('service.models.datasf.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(MOCK_DATASF_JSON)
        response = datasf.filter('https://data.sfgov.org/resource/wwmu-gmzc.json')

    assert response
    assert isinstance(response, list)
    assert len(response) == len(json.loads(MOCK_DATASF_JSON))

def test_datasf_filter_e2e():
    """ Test DataSF filter """
    datasf = DataSF()
    response = datasf.filter('https://data.sfgov.org/resource/wwmu-gmzc.json')
    assert response
    assert isinstance(response, list)

def test_datasf_filter_error():
    """ Test DataSF filter error state """
    datasf = DataSF()
    response = datasf.filter('https://data.sfgov.org/resource/stuff.json')
    assert not response
