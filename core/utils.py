import requests
from datetime import datetime


class Api(object):
    API_URL = 'https://api.exchangeratesapi.io/{endpoint}{params}'
    API_URL2 = lambda self, endpoint: 'http://data.fixer.io/api/{}?access_key=a29e7bf7fd2e4431c46f79442be00b51'.format(endpoint)

    endpoints = {
        'latest': 'latest',
        'history': 'history',
    }
    params = {
        'base': 'base',
        'symbols': 'symbols',
        'start': 'start_at',
        'end': 'end_at',
    }
    DATE_FORMAT = '%Y-%m-%d'
    MIN_YEAR = 1999
    supported_currencies = None

    def __init__(self):
        rates = self.get_rates()['rates']
        self.supported_currencies = [cur for cur in rates]

    def _get_api_url(self, base, target_list, start_date, end_date):

        endpoint = ''
        params = ''
        if start_date and end_date:
            endpoint = self.endpoints['history']
            params = '?{}={}&{}={}'.format(self.params['start'], start_date,
                                           self.params['end'], end_date)
        elif start_date:
            endpoint = start_date
        else:
            # latest
            endpoint = self.endpoints['latest']
        if base:
            base_params = '{}={}'.format(self.params['base'], base)
            if params != '':
                params += '&'
            else:
                params = '?'
            params += base_params
        if target_list:
            if params != '':
                params += '&'
            else:
                params = '?'
            params += "symbols={}".format(",".join(target_list))
        return self.API_URL.format(endpoint=endpoint, params=params)

    def _check_date_format(self, date):

        if date:
            return datetime.strptime(date, self.DATE_FORMAT)

    def get_rates(self, base=None, target_list=[],
                  start_date=None, end_date=None):

        self._check_date_format(start_date)
        self._check_date_format(end_date)
        url = self._get_api_url(base, target_list, start_date, end_date)
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.json()['error']

    def get_rate(self, base='EUR', target='USD',
                 start_date=None, end_date=None):
        res = self.get_rates(base=base, target_list=[target],
                             start_date=start_date, end_date=end_date)
        if end_date:
            return res['rates']
        return res['rates'][target]

    def is_currency_supported(self, currency):
        return currency in self.supported_currencies

    def get_currencies_with_countries(self):
        resp = requests.get(self.API_URL2('symbols'))
        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.json(['error'])









