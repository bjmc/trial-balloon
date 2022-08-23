import requests as requests


class DCVotingInformationAPIClient:
    def __init__(self, api_key, base_url: str = None):
        self.api_key = api_key
        if not base_url:
            base_url = 'https://developers.democracyclub.org.uk/api/v1'
        self.base_url = base_url
        self.default_params = {'auth_token': self.api_key}

    def _lookup(self, endpoint: str, params: dict = None):
        '''
        Call the endpoint and return the response
        '''
        if params:
            self.default_params.update(params)
        req = requests.get(f'{self.base_url}/{endpoint}', params=self.default_params)
        req.raise_for_status()
        return req.json()

    def get_postcode(self, postcode):
        # [validate postcode]
        return self._lookup(f'postcode/{postcode}/')

    def get_address(self, uprn):
        # [validate uprn]
        return self._lookup(f'address/{uprn}/')
