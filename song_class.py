from pydub import AudioSegment
from pydub.playback import play


class Song:
    def __init__(self, song, name, added_at, from_begin, from_end, way, sound):
        self.format = format
        self.name = name
        self.added_at = added_at
        self.end = from_end
        self.begin = from_begin
        self.way = way
        self.sound = sound
        self.song = song
        self.song += sound
        if way:
            self.song = self.song.reverse()
