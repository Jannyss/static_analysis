from typing import Optional
from yandex_music import Client, Track


class YandexMusicAPI:

    def __init__(self):
        self.client = Client()

    def search_track_id(self, artist: str, title: str) -> Optional[str]:
        query = f'{artist} {title}'
        search_result = self.client.search(query).best
        if search_result:
            if type(search_result.result) == Track:
                return search_result.result.track_id

    def get_lyrics_old(self, track_id: str) -> Optional[str]:
        lyrics = self.client.track_supplement(track_id).lyrics
        if lyrics:
            return lyrics.full_lyrics

    def get_lyrics(self, artist: str, title: str):
        query = f'{artist} {title}'
        search_result = self.client.search(query).best
        if search_result:
            if type(search_result.result) == Track:
                lyrics = search_result.result.get_supplement().lyrics
                if lyrics:
                    return lyrics.full_lyrics
