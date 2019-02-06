from pydub import AudioSegment
import pydub.playback
from song_class import Song
import pygame
import interface


def expo(timeln, filename):
    if timeln:
        melody_length = max(timeln, key=lambda x: x.end)
    else:
        melody_length = 0
    res = AudioSegment.silent(duration=(melody_length.end + 1000))
    res = res.set_channels(2)
    for i in timeln:
        res = res.overlay(i.song, position=i.added_at)
    res.export(filename + '.mp3', format='mp3')


def play_track(timeln):
    global p
    pygame.init()
    if timeln:
        melody_length = max(timeln, key=lambda x: x.end)
        res = AudioSegment.silent(duration=(melody_length.end + 1000))
        res = res.set_channels(2)
        for i in timeln:
            res = res.overlay(i.song, position=i.added_at)
        res.export('example.mp3', format='mp3')
        pygame.mixer.music.load('example.mp3')
        pygame.mixer.music.play()


def stop_playing():
    pygame.mixer.music.stop()
