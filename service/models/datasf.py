"""DataSF model"""
import requests

class DataSF():
    """DataSF model class"""
    @staticmethod
    def filter(endpoint, filters=None, headers=None):
        """https://dev.socrata.com/docs/filtering.html"""
        try:
            request = requests.get(endpoint, params=filters, headers=headers)
            if request.status_code == 200:
                response = request.json()
            return response
        # pylint: disable=bare-except
        except:
            return None
        