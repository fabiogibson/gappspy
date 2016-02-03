from services.core import GoogleService, GoogleCredentials
from mock import patch, Mock, MagicMock, mock_open
import apiclient
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
import __builtin__


class TestGoogleService(object):

    @patch("apiclient.discovery.build")
    def test_constructor(self, mock_build):
        # mock
        mock_credentials = MagicMock()

        # act
        service = GoogleService("gmail", "v1", mock_credentials)

        # assert
        assert service is not None
        mock_build.assert_called_once_with(
            "gmail", "v1", http=mock_credentials.authorize())


class TestGoogleCredentials(object):

    @patch.object(GoogleCredentials, '_read_private_key', return_value="keyfile")
    def setUp(self, mock_read_private_key):
        """
        """
        self.credentials = GoogleCredentials("service_account", "keyfile", "permission", "impersonate_as")

    @patch.object(SignedJwtAssertionCredentials, '__init__', return_value=None)
    @patch.object(GoogleCredentials, '_read_private_key', return_value="keyfile")
    def test_constructor(self, mock_credentials, mock_signed_credentials):
        # mock
        credentials = GoogleCredentials("service_account", "keyfile", "permission", "impersonate_as")

        # assert
        assert self.credentials.auth_url == 'https://www.googleapis.com/auth/%s'
        assert self.credentials.impersonate_as == "impersonate_as"
        assert self.credentials.service_account == "service_account"
        assert self.credentials.private_key == "keyfile"

        mock_signed_credentials.assert_called_with(
            "service_account", "keyfile", 'https://www.googleapis.com/auth/permission', sub="impersonate_as")

    @patch.object(SignedJwtAssertionCredentials, 'authorize', return_value=None)
    @patch('httplib2.Http', spec=True)
    def test_authorize_should_invoke_authorize_credentials(self, mock_http, mock_signed_credentials):
        # act
        self.credentials.authorize()

        # assert
        mock_signed_credentials.assert_called_with(mock_http())

    @patch.object(SignedJwtAssertionCredentials, 'authorize', return_value=None)
    def test_authorize_should_not_invoke_authorize_when_authorized(self, mock_signed_credentials):
        self.credentials.authorization = object

        # act
        self.credentials.authorize()

        # assert
        mock_signed_credentials.assert_not_called()

    @patch.object(__builtin__, 'open', mock_open(read_data="key"))
    def test_read_private_key(self):
        # act
        credentials = GoogleCredentials("service_account", "keyfile", "permission", "impersonate_as")

        # assert
        open.assert_called_once_with("keyfile")
        assert credentials.private_key == "key"
