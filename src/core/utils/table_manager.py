import os
import threading
from pytube import Stream, YouTube, Playlist

from ..utils.table_videos import process_data
from ..widgets.table import Table
from ..widgets.progressbar import Progressbar


class TableManager:
    def __init__(self, table: Table):
        self.table = table
        self.directory = ''
        self.videos: set[str] = set()
        self.streams_to_load: dict[int, Stream] = {}

    def add(self, url: str, directory: str, progressbar: Progressbar, only_audio: bool) -> None:
        self.directory = self.table.directory = directory

        if url.__contains__('list'):
            self._add_playlist(url, progressbar, only_audio)
        else:
            self._add_video(YouTube(url), only_audio)

    def download(self) -> None:
        download_thread = threading.Thread(target=self._download_table, daemon=True)
        download_thread.start()

    def _download_table(self) -> None:
        for item in self.table.get_children():
            if not self.streams_to_load.__contains__(int(item)):
                continue

            self._download_item(item)

    def _download_item(self, item: str) -> None:
        path = self.streams_to_load[int(item)].download(self.directory)

        if os.path.isfile(path):
            self.table.set(item, 'download', '100%')
            self.table.item(item, tags="done")

        del self.streams_to_load[int(item)]

    def _add_playlist(self, url: str, progressbar: Progressbar, only_audio: bool) -> None:
        playlist = Playlist(url)
        progressbar.show(len(playlist.video_urls), only_audio)

        for index, url in enumerate(playlist):
            progressbar.set_value(index)
            self._add_video(YouTube(url), only_audio)

        progressbar.hide()

    def _add_video(self, video: YouTube, only_audio: bool) -> None:
        if self.videos.__contains__(video.title):
            return

        process_data(self.table, self.streams_to_load, video, only_audio)
        self.videos.add(video.title)
        self.table.update()

    def clear_table(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        self.videos.clear()
