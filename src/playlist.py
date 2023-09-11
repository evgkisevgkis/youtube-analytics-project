import os
from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """Класс для плейлистов"""
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist_response = youtube.playlists().list(part='id, contentDetails, snippet',
                                                                                 id=self.playlist_id).execute()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.title = self.playlist_response['items'][0]['snippet']['title']
