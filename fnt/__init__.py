"""REST client for FNT Command (https://www.fntsoftware.com/en/products/fnt-command)"""

import requests

VERSION = '0.0.2'


class UnsuccessfulStatusResponse(Exception):
    """json response body contains status.success == False"""
    def __init__(self, status):
        self.message = status['message']
        self.error_code = status['errorCode']
        self.sub_error_code = status['subErrorCode']

    def __str__(self):
        return f'{self.message} ({self.error_code}, {self.sub_error_code})'


class RESTClient:
    def __init__(self, **kwargs):
        self.config = kwargs
        self.base_url = self.config['server']
        self.base_path = '/axis/api/rest'

    def _get(self, path, response_key):
        """REST GET"""
        req = requests.get(f'{self.base_url}{self.base_path}{path}')
        req.raise_for_status()
        res = req.json()
        if not res['status']['success']:
            raise UnsuccessfulStatusResponse(res['status'])
        return res[response_key]

    def id(self):
        """Query business gateway ID"""
        return self._get('/businessGateway/Id', 'identifier')

    def systems(self):
        """Query business gateway systems"""
        return self._get('/businessGateway/Systems', 'systems')
