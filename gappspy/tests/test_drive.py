from mock import patch, Mock, MagicMock
from gappspy.core import GoogleCredentials, GoogleService
from gappspy.drive import DriveService
from email.mime.text import MIMEText
from apiclient.http import MediaFileUpload
import base64


class TestDriveService(object):

    @patch.object(GoogleCredentials, '_read_private_key', return_value="keyfile")
    def setUp(self, mock_credentials):
        """
        """
        self.credentials = GoogleCredentials("service_account", "keyfile", "permission", "impersonate_as")

    def test_constructor(self):
        # mock
        with patch.object(GoogleService, "__init__", return_value=None) as mock_constructor:
            drive_service = DriveService(self.credentials)

            # assert
            mock_constructor.assert_called_with('drive', 'v3', self.credentials)

    def test_create_metadata(self):
        with patch.object(GoogleService, "__init__", return_value=None) as mock_constructor:
            drive_service = DriveService(self.credentials)

            # act
            file_metadata = drive_service.create_file_metadata("filename", "mimetype")

            # assert
            assert file_metadata["name"] == "filename"
            assert file_metadata["mimeType"] == "mimetype"

    @patch.object(MediaFileUpload, "__init__", return_value=None)
    def test_create_media(self, mock_fileupload):
        # mock
        with patch.object(GoogleService, "__init__", return_value=None) as mock_constructor:
            drive_service = DriveService(self.credentials)

            # act
            media = drive_service.create_media("filename", "mimetype")

            # assert
            assert isinstance(media, MediaFileUpload)
            mock_fileupload.assert_called_with("filename", mimetype="mimetype", resumable=True)

    @patch("googleapiclient.http.MediaFileUpload", spec=True, return_value=Mock)
    @patch("apiclient.discovery.build")
    def test_create_file(self, mock_build, mock_fileupload):
        # mock
        drive_service = DriveService(self.credentials)

        with patch.object(drive_service.service.files(), 'create', return_value=Mock()) as mock_create_file:
            file_metadata = {
                "name": "filename",
                "mimeType": "mimetype"
            }

            # act
            drive_service.create_file("filename", "mimetype")

            # assert
            mock_create_file.assert_called_with(body=file_metadata, fields="id", media_body=mock_fileupload())

    @patch("apiclient.discovery.build")
    def test_list_files(self, mock_build):
        # mock
        drive_service = DriveService(self.credentials)

        with patch.object(drive_service.service.files(), 'list', return_value=MagicMock()) as mock_list_files:
            # act
            drive_service.list_files()

            # assert
            mock_list_files.assert_called_with(fields='nextPageToken, files(id, name)', pageSize=10)
