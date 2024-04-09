import subprocess
import os
from tkinter.ttk import Treeview

from pytube import YouTube, Stream

from .youtube import get_stream


def get_row_data(_id: int, video: YouTube, stream: Stream) -> tuple:
    return _id, video.title, video.author, parse_time(video.length), bytes_to_mb(stream.filesize), '0%'


def parse_time(length: int):
    return f'{int(length / 60)}:{"0" + str(length % 60) if length % 60 < 10 else length % 60}'


def bytes_to_mb(_bytes: int):
    return round(_bytes / (1024 * 1024), 2)


def open_directory(path: str):
    if os.path.isfile(path + '.mp4'):
        open_explorer(f'{path}.mp4')
    else:
        open_explorer(f'{path}.webm')


def open_explorer(path: str):
    explorer_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.run([explorer_path, '/select,', os.path.normpath(path)])


def process_data(table: Treeview, streams: dict[int, Stream], video: YouTube, only_audio: bool):
    _id = len(table.get_children())
    register_callback(table, _id, video)

    _stream = get_stream(video, only_audio=only_audio)
    _data = get_row_data(_id, video, _stream)
    table.insert(parent='', index='end', iid=_id, text='', values=_data)

    print(f'Added video: {_data[1]}')

    streams[_id] = _stream


def register_callback(table: Treeview, index: int, video: YouTube):
    video.register_on_progress_callback(
        lambda stream, chunk, bytes_remaining: progress_function(table, index, stream, bytes_remaining))


def progress_function(table: Treeview, _id, stream, bytes_remaining):
    value = round((1 - bytes_remaining / stream.filesize) * 100, 0)
    table.set(_id, 'download', str(value) + '%')
    table.update()
