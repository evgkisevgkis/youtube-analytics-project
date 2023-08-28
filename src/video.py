import json
import os
from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео"""
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_response = youtube.videos().list(part='snippet,'
                                                         'statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/{self.video_id}'
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']


class PLVideo(Video):
    """Класс для видео с инициализацией через ссылку на плей лист"""
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
