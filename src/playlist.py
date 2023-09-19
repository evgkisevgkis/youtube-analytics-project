import os
from googleapiclient.discovery import build
from datetime import timedelta
from isodate import parse_duration


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
        self.playlist_items_response = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                    part='id, contentDetails, snippet',
                                                                    maxResults=50,
                                                                    ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId']
                                     for video in self.playlist_items_response['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

    @property
    def total_duration(self):
        counter = timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = parse_duration(iso_8601_duration)
            counter += duration
        return counter
