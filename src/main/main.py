import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

# ===================== TRACK =====================
class Track:
    def __init__(self, name):
        self.name = name
        self.data = []
        self.muted = False
        self.volume = 1.0

    def add_chunk(self, chunk):
        self.data.append(chunk.copy())

    def get_audio(self):
        if not self.data:
            return np.array([])
        audio = np.concatenate(self.data, axis=0)
        return audio * self.volume if not self.muted else np.zeros_like(audio)

# ===================== AUDIO ENGINE =====================
class AudioEngine:
    def __init__(self):
        self.samplerate = 44100
        self.channels = 2
        self.tracks = []
        self.current_track = None
        self.recording = False
        self.monitoring = False
        self.stream = None
        self.input_device = None
        self.output_device = None

    def new_track(self):
        track = Track(f"Track {len(self.tracks)+1}")
        self.tracks.append(track)
        self.current_track = track

    def callback(self, indata, outdata, frames, time, status):
        if self.recording and self.current_track:
            self.current_track.add_chunk(indata)
        if self.monitoring:
            outdata[:] = indata
        else:
            outdata.fill(0)

    def start(self):
        self.stream = sd.Stream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self.callback,
            device=(self.input_device, self.output_device)
        )
        self.stream.start()

    def restart(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.start()

    def export(self, filename):
        mix = sum([t.get_audio() for t in self.tracks if t.get_audio().size > 0])
        if mix.size > 0:
            sf.write(filename, mix, self.samplerate)

# ===================== UI =====================
class ModernUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCord v1.0")
        self.resize(1000, 600)

        self.engine = AudioEngine()

        layout = QtWidgets.QVBoxLayout()

        # === Device selection ===
        device_layout = QtWidgets.QHBoxLayout()

        self.input_select = QtWidgets.QComboBox()
        self.output_select = QtWidgets.QComboBox()

        device_layout.addWidget(QtWidgets.QLabel("Entrée"))
        device_layout.addWidget(self.input_select)
        device_layout.addWidget(QtWidgets.QLabel("Sortie"))
        device_layout.addWidget(self.output_select)

        # Load devices
        self.devices = sd.query_devices()
        for i, dev in enumerate(self.devices):
            if dev['max_input_channels'] > 0:
                self.input_select.addItem(dev['name'], i)
            if dev['max_output_channels'] > 0:
                self.output_select.addItem(dev['name'], i)

        self.input_select.currentIndexChanged.connect(self.change_device)
        self.output_select.currentIndexChanged.connect(self.change_device)

        # === Timeline ===
        self.plot = pg.PlotWidget()
        self.plot.setBackground('#121212')
        self.plot.showGrid(x=True, y=True)

        # === Controls ===
        self.btn_github = QtWidgets.QPushButton("GitHub")
        self.btn_github.setStyleSheet("""
            QPushButton {
                background-color: #24292e;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        controls = QtWidgets.QHBoxLayout()
        self.btn_record = QtWidgets.QPushButton("● Record")
        self.btn_stop = QtWidgets.QPushButton("■ Stop")
        self.btn_new = QtWidgets.QPushButton("+ Track")
        self.btn_export = QtWidgets.QPushButton("Export WAV")
        self.btn_monitor = QtWidgets.QPushButton("Monitoring")

        for b in [self.btn_record, self.btn_stop, self.btn_new, self.btn_export, self.btn_monitor, self.btn_github]:
            b.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
            """)
            controls.addWidget(b)

        layout.addLayout(device_layout)
        layout.addWidget(self.plot)
        layout.addLayout(controls)
        self.setLayout(layout)

        # GitHub button action
        self.btn_github.clicked.connect(self.open_github)

        # Connections
        self.btn_new.clicked.connect(self.new_track)
        self.btn_record.clicked.connect(self.record)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_export.clicked.connect(self.export)
        self.btn_monitor.clicked.connect(self.toggle_monitor)

        # Start engine
        self.change_device()

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_waveform)
        self.timer.start(100)

    def change_device(self):
        self.engine.input_device = self.input_select.currentData()
        self.engine.output_device = self.output_select.currentData()
        self.engine.restart()

    def new_track(self):
        self.engine.new_track()

    def record(self):
        if not self.engine.current_track:
            self.engine.new_track()
        self.engine.recording = True

    def stop(self):
        self.engine.recording = False

    def toggle_monitor(self):
        self.engine.monitoring = not self.engine.monitoring

    def export(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export", "", "WAV (*.wav)")
        if file:
            self.engine.export(file)

    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/Isax820/PyCord")

    def update_waveform(self):
        self.plot.clear()
        for track in self.engine.tracks:
            audio = track.get_audio()
            if audio.size > 0:
                self.plot.plot(audio[:,0], pen=pg.mkPen(width=1))

# ===================== MAIN =====================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(18,18,18))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    app.setPalette(palette)

    window = ModernUI()
    window.show()

    sys.exit(app.exec_())