from pytube import YouTube, Stream, StreamQuery


def get_streams(video: YouTube, only_audio: bool) -> StreamQuery:
    return video.streams.filter(only_audio=only_audio)


def get_stream(video: YouTube, only_audio: bool = True) -> Stream:
    streams = get_streams(video, only_audio)
    return get_first(streams)


def get_first(stream: StreamQuery) -> Stream: return stream.order_by('abr').desc().first()
