# 🎛️ PyCord — Python Audio Workstation

> ⚡ A modern, minimal, and powerful Digital Audio Workstation built in Python
>
> 🎧 Real-time audio • 🎚️ Multi-track • 🎨 Modern UI • 🔊 Live monitoring

---

## ✨ Features

* 🎵 **Multi-track recording** — record unlimited audio tracks
* 🎚️ **Real-time waveform timeline**
* 🎤 **Audio input/output selection**
* 🔊 **Live monitoring (zero-latency feel)**
* 💽 **Export WAV (mixdown)**
* 🌙 **Modern dark UI (inspired by FL Studio)**

---

## 🚀 Demo

```bash
python main.py
```

---

## 📦 Installation

```bash
pip install sounddevice soundfile PyQt5 pyqtgraph numpy
```

---

## 🧠 Architecture

```
AudioEngine
 ├── Tracks[]
 │    ├── audio buffers
 │    ├── volume / mute
 │
 ├── Input Stream (microphone)
 ├── Output Stream (monitoring)
 └── Real-time processing callback
```

---

## 🎧 Monitoring Explained

Monitoring lets you hear your microphone **in real-time** while recording.

```python
outdata[:] = indata
```

⚠️ Use headphones to avoid feedback.

---

## 🎨 UI Preview

* Dark mode 🌑
* Smooth buttons
* Real-time waveform

---

## 🛠️ Roadmap

* [ ] 🎼 Drag & drop timeline (clips)
* [ ] 🎛️ Mixer (volume / pan / effects)
* [ ] 📊 VU meters
* [ ] 🎧 Low-latency engine improvements
* [ ] 💽 MP3 export
* [ ] 🧲 Zoom & scroll timeline

---

## 💡 Why this project?

Because building audio software is **fun, hard, and insanely satisfying**.

This project is a step toward a **fully custom DAW** — from scratch.

---

## ⚡ Tech Stack

* Python 🐍
* PyQt5 (UI)
* sounddevice (audio I/O)
* numpy (audio processing)
* pyqtgraph (visualization)

---

## 🤝 Contributing

Pull requests are welcome.

If you want to build a **next-gen Python DAW**, you're in the right place.

---

## 🧠 Inspiration

* FL Studio
* Ableton Live
* Logic Pro

---

## ⭐ Support

If you like this project:

👉 Star the repo
👉 Share it
👉 Build something crazy with it

---

## ⚠️ Disclaimer

This is an experimental project — not production-ready (yet).

---

## 🧬 Future Vision

> A fully modular, open-source DAW powered by Python.

---

# 🚀 Built with passion + caffeine
