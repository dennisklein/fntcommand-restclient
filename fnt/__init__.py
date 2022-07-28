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

    def id(self):
        """Query business gateway ID"""
        path = f'{self.base_path}/businessGateway/Id'
        req = requests.get(f'{self.base_url}{path}')
        req.raise_for_status()
        res = req.json()
        if not res['status']['success']:
            raise UnsuccessfulStatusResponse(res['status'])
        return res['identifier']

    def systems(self):
        """Query business gateway systems"""
        path = f'{self.base_path}/businessGateway/Systems'
        req = requests.get(f'{self.base_url}{path}')
        req.raise_for_status()
        res = req.json()
        if not res['status']['success']:
            raise UnsuccessfulStatusResponse(res['status'])
        return res['systems']
