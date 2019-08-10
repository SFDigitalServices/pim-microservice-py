"""Tests for Records resource"""
from service.models.datasf import DataSF

def test_datasf_filter():
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
