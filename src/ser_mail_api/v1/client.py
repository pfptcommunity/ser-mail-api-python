"""
Author: Ludvik Jerabek
Package: ser_mail_api
License: MIT
"""
from requests.adapters import HTTPAdapter
from requests_oauth2client import OAuth2Client, OAuth2ClientCredentialsAuth

from ser_mail_api.v1.endpoints.send import Send
from ser_mail_api.v1.resources.error_handler import ErrorHandler
from ser_mail_api.v1.resources.resource import Resource


class TimeoutHTTPAdapter(HTTPAdapter):
    timeout = None

    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None and hasattr(self, 'timeout'):
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Client(Resource):
    __api_token: str
    __error_handler: ErrorHandler
    __send: Send

    def __init__(self, client_id: str, client_secret: str):
        super().__init__(None, "https://mail.ser.proofpoint.com/v1")

        self.__error_handler = ErrorHandler()
        self._session.hooks = {"response": self.__error_handler.handler}

        # Deal with OAuth2
        oauth2_client = OAuth2Client("https://mail.ser.proofpoint.com/v1/token", auth=(client_id, client_secret))
        oauth2_client.client_credentials({"grant_type": "client_credentials"})
        self._session.auth = OAuth2ClientCredentialsAuth(oauth2_client, scope="client_credentials")
        self.__send = Send(self, 'send')

    @property
    def send(self) -> Send:
        return self.__send

    @property
    def timeout(self):
        return self._session.adapters.get('https://').timeout

    @timeout.setter
    def timeout(self, timeout):
        self._session.adapters.get('https://').timeout = timeout

    @property
    def error_handler(self) -> ErrorHandler:
        return self.__error_handler

    @error_handler.setter
    def error_handler(self, error_handler: ErrorHandler):
        self.__error_handler = error_handler
