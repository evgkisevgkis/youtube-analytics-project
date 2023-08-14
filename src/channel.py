import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id = self.channel["items"][0]["id"]
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/{self.channel["items"][0]["snippet"]["customUrl"]}'
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        """Возвращает название канала и ссылку на него"""
        return f"{self.title} ({self.url})"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        lines = [self.id, self.title, self.description,
                 self.url, self.subscriber_count, self.video_count, self.view_count]
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines("%s\n" % line for line in lines)
