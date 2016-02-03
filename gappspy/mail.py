from core import GoogleService
from email.mime.text import MIMEText
import base64


class GmailMessage(object):

    def __init__(self, from_addr, to_addr, subject, message):
        """

        """
        self._message = MIMEText(message)
        self._message['from'] = from_addr
        self._message['to'] = to_addr
        self._message['subject'] = subject

    def raw(self):
        """
        """
        return {'raw': base64.urlsafe_b64encode(self._message.as_string())}


class GmailService(GoogleService):

    def __init__(self, credentials):
        """
        """
        super(GmailService, self).__init__('gmail', 'v1', credentials)

    def send_mail(self, message):
        """
        """
        send_message = self.service.users().messages().send(userId="me", body=message.raw())
        send_message.execute()
