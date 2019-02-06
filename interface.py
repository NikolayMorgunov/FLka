import sys
from pydub import AudioSegment
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QComboBox, QLabel, QFileDialog)
from PyQt5.QtGui import QPen
import PyQt5.QtGui as QtGui
import main, song_class
import export

time_line = []
time_line_names = []


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('FLka')

        self.import_btn = QPushButton('Добавить трек', self)
        self.import_btn.resize(self.import_btn.sizeHint())
        self.import_btn.move(20, 360)
        self.import_btn.clicked.connect(self.adding_track)

        self.ex_btn = QPushButton('Экспорт', self)
        self.ex_btn.resize(self.ex_btn.sizeHint())
        self.ex_btn.move(170, 360)
        self.ex_btn.clicked.connect(self.to_exp)

        self.pl_btn = QPushButton('Воспроизвести', self)
        self.pl_btn.resize(self.pl_btn.sizeHint())
        self.pl_btn.move(320, 360)
        self.pl_btn.clicked.connect(self.to_play)

        self.st_btn = QPushButton('Остановить', self)
        self.st_btn.resize(self.st_btn.sizeHint())
        self.st_btn.move(470, 360)
        self.st_btn.clicked.connect(self.to_stop)

        self.changing_lbl = QLabel("Изменить трек", self)
        self.changing_lbl.move(200, 25)

        self.choose_track = QComboBox(self)
        self.choose_track.addItems(time_line_names)
        self.choose_track.move(200, 50)

        self.choose_param = QComboBox(self)
        self.choose_param.addItems(['Громкость', 'Место', 'Сменить направление', 'Удалить'])
        self.choose_param.move(200, 110)

        self.ch_btn = QPushButton('Изменить', self)
        self.ch_btn.resize(self.ch_btn.sizeHint())
        self.ch_btn.move(200, 170)
        self.ch_btn.clicked.connect(self.change_track)

        self.del_bnt = QPushButton('Начать проект заново', self)
        self.del_bnt.resize(self.del_bnt.sizeHint())
        self.del_bnt.move(200, 270)
        self.del_bnt.clicked.connect(self.del_all)

        self.lengths = []
        self.timeln_str = []
        self.timeln_labels = []

    def adding_track(self):
        # путь
        fname = QFileDialog.getOpenFileName(self, 'Выберите файл', '/home', "*.wav *.mp3")[0]

        if not fname:
            return
        try:
            new_song = AudioSegment.from_wav(fname)
        except Exception:
            new_song = AudioSegment.from_mp3(fname)
        # путь
        text, ok = QInputDialog.getText(self, 'Имя', 'Введите имя трека')
        uniq = False
        while not uniq and ok:
            uniq = True
            for i in time_line:
                if i.name == text:
                    uniq = False
                    text, ok = QInputDialog.getText(self, 'Такое имя уже есть', 'Введите имя трека')
                    break
            if len(text.split()) != 1:
                uniq = False
                text, ok = QInputDialog.getText(self, 'Имя должно содержать одно слово', 'Введите имя трека')
        # начало
        len_sec = len(new_song) / 1000
        fname = text
        if ok:
            file_name = text
            text, ok = QInputDialog.getText(self, 'Начало',
                                            'Введите начало отрезка (от 0 до ' + str(len_sec) + ')')
        while ok and valid_val(text, 0, len_sec):
            text, ok = QInputDialog.getText(self, valid_val(text, 0, len_sec),
                                            'Введите начало отрезка (от 0 до ' + str(len_sec) + ')')
            # конец

        if ok:
            beg = float(text)
            text, ok = QInputDialog.getText(self, 'Конец', 'Введите конец отрезка (от ' + str(beg) +
                                            ' до' + str(len_sec) + ')')
            while ok and valid_val(text, beg, len_sec):
                text, ok = QInputDialog.getText(self, valid_val(text, beg, len_sec),
                                                'Введите конец отрезка (от ' + str(beg) + ' до ' + str(
                                                    len_sec) + ')')

            if ok:
                end = float(text)
                # куда вставить
                text, ok = QInputDialog.getText(self, 'Вставка', 'На какой секунде вставить отрывок')
                while ok and valid_val(text, 0, 2000000000):
                    text, ok = QInputDialog.getTextQInputDialog.getText(self,
                                                                        valid_val(text, 0, 2000000000),
                                                                        'На какой секунде вставить отрывок')
                if ok:
                    add_at = float(text)
                    time_line.append(
                        song_class.Song(new_song, fname, add_at * 1000, beg * 1000,
                                        end * 1000, False, 0))
                    time_line_names.append(fname)
                    self.choose_track.addItem(fname)

    def to_exp(self):
        text, ok = QInputDialog.getText(self, 'Экспорт', 'Введите имя нового файла без расширения')
        if ok:
            export.expo(time_line, text)

    def to_play(self):
        export.play_track(time_line)

    def to_stop(self):
        export.stop_playing()

    def change_track(self):
        if self.choose_track.currentText() and self.choose_param.currentText() == 'Громкость':
            text, ok = QInputDialog.getText(self, 'Изменить громкость трека',
                                            'На сколько децибел увеличить громкость (уменьшить при отрицательном значении)')
            norm_val = False
            while not norm_val and ok:
                try:
                    text = int(text)
                    norm_val = True
                except ValueError:
                    text, ok = QInputDialog.getText(self, 'Введите целое число',
                                                    'На сколько децибел увеличить громкость (уменьшить при отрицательном значении)')
                if ok and norm_val:
                    for i in time_line:
                        if i.name == self.choose_track.currentText():
                            i.song += int(text)
                            i.sound += int(text)
                            break
        elif self.choose_track.currentText() and self.choose_param.currentText() == 'Место':
            text, ok = QInputDialog.getText(self, 'Изменить положение',
                                            'На сколько миллисекунд сместить трек вперёд громкость (назад при отрицательном значении)')
            norm_val = False
            while not norm_val and ok:
                try:
                    text = int(text)
                    norm_val = True
                except ValueError:
                    text, ok = QInputDialog.getText(self, 'Введите целое число',
                                                    'На сколько миллисекунд сместить трек вперёд громкость (назад при отрицательном значении)')
                if ok and norm_val:
                    for i in time_line:
                        if i.name == self.choose_track.currentText():
                            i.added_at += int(text)
                            if i.added_at < 0:
                                i.added_at = 0
                            break

        elif self.choose_track.currentText() and self.choose_param.currentText() == 'Сменить направление':
            for i in time_line:
                if i.name == self.choose_track.currentText():
                    i.song = i.song.reverse()
                    i.way = not i.way
                    break

        elif self.choose_track.currentText():
            for i in range(len(time_line)):
                if time_line[i].name == self.choose_track.currentText():
                    del time_line[i]
                    del time_line_names[i]
                    self.choose_track.removeItem(i)
                    break

    def del_all(self):
        global time_line
        global time_line_names
        n = len(time_line)
        time_line = []
        time_line_names = []
        for i in range(n):
            self.choose_track.removeItem(0)


def valid_val(n, left, right):
    try:
        n = float(n)
    except ValueError:
        return 'Неверный тип'
    if not (left <= n <= right):
        return 'Значение не в нужном интервале'
