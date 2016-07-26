import datetime

from .base import BaseEndpoint
from ..exceptions import LoginError, APIError


class Login(BaseEndpoint):

    _error = LoginError
    _endpoints_uk = {
        'Login': 'https://identitysso.betfair.com/api/certlogin'
    }

    def __call__(self):
        payload = 'username=' + self.client.username + '&password=' + self.client.password
        url = self._endpoints_uk['Login']
        (response, raw_response, sent) = self.request(url, payload)
        self.client.set_session_token(response.get('sessionToken'))
        return response

    def request(self, url, payload=None, params=None, session=None):
        if not session:
            session = self.client.session
        date_time_sent = datetime.datetime.now()
        try:
            response = session.post(url, data=payload, headers=self.client.login_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, params, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, params, exception=e)
        return self.create_resp(response, date_time_sent)

    def _error_handler(self, response, params=None, method=None):
        if response.get('loginStatus') != 'SUCCESS':
            raise self._error(response)
