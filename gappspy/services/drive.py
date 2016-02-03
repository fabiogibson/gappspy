from core import GoogleService
import apiclient


class DriveService(GoogleService):

    def __init__(self, credentials):
        """

        """
        super(DriveService, self).__init__('drive', 'v3', credentials)

    def list_files(self, page_size=10):
        """
        """
        list_service = self.service.files().list(pageSize=page_size, fields="nextPageToken, files(id, name)")
        results = list_service.execute()
        return results.get('files', [])

    def create_file_metadata(self, file_name, mime_type):
        """
        """
        return {
            'name': file_name,
            'mimeType': mime_type
        }

    def create_media(self, file_name, mime_type, resumable=True):
        """
        """
        return apiclient.http.MediaFileUpload(file_name, mimetype=mime_type, resumable=resumable)

    def create_file(self, file_name, mime_type):
        """
        """
        file_metadata = self.create_file_metadata(file_name, mime_type)
        media = self.create_media(file_name, mime_type)

        create_service = self.service.files().create(body=file_metadata, media_body=media, fields='id')
        create_service.execute()
