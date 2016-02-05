import apiclient
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials


class GoogleCredentials(object):

    def _read_private_key(self, keyfile):
        """

        """
        with open(keyfile) as f:
            return f.read()

    def __init__(self, service_account, keyfile, permission, impersonate_as):
        """

        """
        self.auth_url = 'https://www.googleapis.com/auth/%s' % permission
        self.impersonate_as = impersonate_as
        self.service_account = service_account
        self.private_key = self._read_private_key(keyfile)
        self.credentials = SignedJwtAssertionCredentials(self.service_account, self.private_key, self.auth_url,
                                                         sub=self.impersonate_as)
        self.authorization = None

    def authorize(self):
        """
        """
        if not self.authorization:
            self.authorization = self.credentials.authorize(httplib2.Http())

        return self.authorization


class GoogleService(object):

    def __init__(self, name, version, credentials):
        """
        """
        self.service = apiclient.discovery.build(name, version, http=credentials.authorize())
