import os
from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео"""
    def __init__(self, video_id: str):
        self.video_id = video_id
        try:
            self.video_response = youtube.videos().list(part='snippet,'
                                                             'statistics,contentDetails,topicDetails',
                                                        id=self.video_id).execute()
            self.video_title: str = self.video_response['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/{self.video_id}'
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']
        except IndexError:
            self.video_response = None
            self.video_title = None
            self.url = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """Класс для видео с плейлистом"""
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
