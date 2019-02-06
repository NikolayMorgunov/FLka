import sys
from pydub import AudioSegment
from pydub.playback import play
from song_class import Song
import interface
import export

if __name__ == "__main__":
    app = interface.QApplication(sys.argv)
    while True:
        ex = interface.Example()
        ex.show()
        sys.exit(app.exec())
