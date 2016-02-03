from mock import patch, Mock, MagicMock
from services.core import GoogleCredentials, GoogleService
from services.mail import GmailService, GmailMessage
from email.mime.text import MIMEText
import base64


class TestGmailMessage(object):

    def test_constructor(self):
        # act
        mock_message = GmailMessage(from_addr="from", to_addr="to", subject="subject", message="message")

        assert isinstance(mock_message._message, MIMEText)
        assert mock_message._message["from"] == "from"
        assert mock_message._message["to"] == "to"
        assert mock_message._message["subject"] == "subject"

    def test_message_raw(self):
        # mock
        message = GmailMessage(from_addr="from", to_addr="to", subject="subject", message="message")

        # act
        message_raw = message.raw()

        # assert
        assert "raw" in message_raw
        assert message_raw["raw"] == base64.urlsafe_b64encode(message._message.as_string())


class TestGmailService(object):

    @patch.object(GoogleCredentials, '_read_private_key', return_value="keyfile")
    def setUp(self, mock_credentials):
        """
        """
        self.credentials = GoogleCredentials("service_account", "keyfile", "permission", "impersonate_as")

    def test_constructor(self):
        with patch.object(GoogleService, "__init__", return_value=None) as mock_constructor:
            # act
            service = GmailService(self.credentials)

            # assert
            mock_constructor.assert_called_with('gmail', 'v1', self.credentials)

    @patch("apiclient.discovery.build")
    def test_send_mail(self, mock_build):
        # mock
        gmail_service = GmailService(self.credentials)

        with patch.object(gmail_service.service.users().messages(), 'send', return_value=Mock()) as mock_send:
            message = MagicMock()

            # act
            gmail_service.send_mail(message)

            # assert
            mock_send.assert_called_with(userId="me", body=message.raw())

