# CaptionFlow

**Real-Time Speech-to-Text and Multi-Language Translation** 🎤 → 🌐

CaptionFlow is an AI-powered live transcription and translation platform that converts spoken audio into captions in multiple Indian languages with real-time processing. Perfect for live streams, meetings, educational content, and accessibility.

---

## ✨ Features

- **Real-Time Transcription**: Convert live audio to English text using Whisper AI
- **Multi-Language Translation**: Translate to 15+ Indian and international languages
- **Streaming Architecture**: Process audio chunks on-the-fly without buffering
- **Live Caption Display**: Spotify-style scrolling captions (max 2 lines visible)
- **Supported Languages**: English, [translate:हिंदी], [translate:तमिल], [translate:বাংলা], [translate:తెలుగు], [translate:ಕನ್ನಡ], [translate:മലയാളം], [translate:मराठी], [translate:ગુજરાતી], [translate:ਪੰਜਾਬੀ], [translate:ଓଡ଼ିଆ], [translate:भोजपुरी], [translate:संस्कृत], and more
- **Minimal UI**: Clean, responsive interface built with React + Tailwind CSS
- **Easy Deployment**: Containerized backend with Docker support

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│            (Vite + Tailwind + Socket.IO)                │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Language Selector | Start/Stop Button          │   │
│  │  Original Text | Translated Output              │   │
│  └─────────────────────────────────────────────────┘   │
└────────────┬────────────────────────────────────────────┘
             │ WebSocket (Socket.IO)
             ▼
┌─────────────────────────────────────────────────────────┐
│                   Flask + Socket.IO                      │
│                   Backend Server                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Audio Input → Whisper (tiny.en) → Transcription │  │
│  │           ↓                                       │  │
│  │ English Text → NLLB-200 → Target Language       │  │
│  │           ↓                                       │  │
│  │ Emit via Socket.IO to Frontend                  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- 8GB+ RAM (for ML models)
- 10GB+ disk space (for model caching)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/ASHUTOSH-A-49/CaptionFlow.git
cd CaptionFlow

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask backend
python app.py
```

Backend will start at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at `http://localhost:5173`

---

## 📦 Installation & Dependencies

### Backend (`requirements.txt`)

```
flask==2.3.0
flask-socketio==5.3.0
flask-cors==4.0.0
sounddevice==0.4.6
numpy==1.24.0
faster-whisper==0.9.0
transformers==4.30.0
torch==2.0.0
python-socketio==5.9.0
```

### Frontend (`package.json`)

```json
{
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "socket.io-client": "^4.5.0",
    "framer-motion": "^12.23.24"
  },
  "devDependencies": {
    "vite": "^7.1.7",
    "tailwindcss": "^4.1.17",
    "@tailwindcss/vite": "^4.1.17"
  }
}
```

---

## 🎯 How It Works

### 1. **Audio Capture**
- Microphone input captured at 16kHz sample rate
- Audio streamed in 0.5-second blocks
- No buffering delays for real-time processing

### 2. **Transcription**
- Whisper (tiny.en) model processes each audio block
- English transcript extracted in real-time
- Segments emitted immediately

### 3. **Translation**
- NLLB-200 (Distilled 600M) model translates to target language
- Supports 15+ Indian languages
- Fallback to original text if target language is English

### 4. **Frontend Display**
- Captions displayed in Spotify-style scrolling format
- Max 2 lines visible at a time
- Newest caption automatically pushes oldest off screen
- Bold, minimalist font styling for readability

---

## 🛠️ Configuration

### Backend (`app.py`)

**Language Codes**:
```python
LANGUAGE_CODE_MAPPING = {
    "en": "eng_Latn",      # English
    "hi": "hin_Deva",      # Hindi
    "ta": "tam_Taml",      # Tamil
    "bn": "ben_Beng",      # Bengali
    "bho": "bho_Deva",     # Bhojpuri
    "san": "san_Deva",     # Sanskrit
    # ... more languages
}
```

**Audio Settings**:
```python
samplerate = 16000          # Sample rate in Hz
block_duration = 0.5        # Audio block size in seconds
chunk_duration = 2          # Processing chunk size in seconds
channels = 1                # Mono audio
```

### Frontend (`Translator.jsx`)

**Language Options**:
```jsx
const languages = [
  { label: "English", value: "eng_Latn" },
  { label: "Hindi", value: "hin_Deva" },
  { label: "Tamil", value: "tam_Taml" },
  { label: "Bhojpuri", value: "bho_Deva" },
  { label: "Sanskrit", value: "san_Deva" },
  // ... add more
];
```

**Socket.IO Connection**:
```jsx
const socket = io("http://localhost:5000");
```

---

## 📡 API & Socket Events

### Socket.IO Events

**Client → Server:**
```javascript
socket.emit("start_transcription", { target_lang: "hin_Deva" });
socket.emit("stop_transcription");
```

**Server → Client:**
```javascript
socket.on("translated_text", {
  original: "Hello, how are you?",
  translated: "[Translation in target language]",
  source_lang: "en",
  source_lang_name: "English",
  target_lang: "hin_Deva",
  target_lang_name: "Hindi"
});
```

---

## 🎨 UI Components

### Pages

1. **Intro Page** (`components/Intro.jsx`)
   - Landing page with feature highlights
   - "Get Started" button with smooth scroll

2. **Translator Page** (`components/Translator.jsx`)
   - Language selection dropdown
   - Start/Stop transcription button
   - Live caption display areas
   - Real-time text updates

3. **Features Section** (`components/FeatureIntro.jsx`)
   - Highlighted key features
   - Alternating layout boxes

4. **Footer** (`components/Footer.jsx`)
   - Credits and branding

### Styling

- **Framework**: Tailwind CSS 4.1+
- **Animations**: Framer Motion
- **Font**: Semi-bold (font-semibold) for captions
- **Color Scheme**: Dark theme (gray-900, indigo accents)

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────┐
│ User speaks into microphone                              │
└─────────────┬───────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────┐
│ sounddevice captures audio at 16kHz                      │
└─────────────┬───────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────┐
│ Audio blocks queued and processed immediately            │
└─────────────┬───────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────┐
│ Whisper (tiny.en) transcribes to English                 │
└─────────────┬───────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────┐
│ NLLB-200 translates to target language                   │
└─────────────┬───────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────┐
│ Socket.IO emits caption data to frontend                 │
└─────────────┬───────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────┐
│ React updates caption display (max 2 lines)              │
│ Oldest caption auto-removes when new one arrives         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Performance Specs

| Metric | Value |
|--------|-------|
| Latency | ~500ms-1s per caption |
| Memory Usage | 3-4GB (with loaded models) |
| Max Concurrent Users | 5-10 (single instance) |
| Supported Languages | 15+ |
| Model Size | Whisper: 140MB, NLLB: 1.2GB |
| CPU Usage | 40-60% per active transcription |

---

## 🐛 Troubleshooting

### Issue: "SARVAM_API_ENDPOINT not found"
**Solution**: This is legacy code. The current version uses local Whisper, not Sarvam API. Remove these environment checks.

### Issue: Microphone access denied
**Solution**: Ensure the app runs over HTTPS in production (required for Web Audio API). Use `http://localhost` for development.

### Issue: Models not loading
**Solution**: Models auto-download on first run. Ensure 10GB+ free disk space. Check internet connection during first startup.

### Issue: High latency on first run
**Solution**: Models are being downloaded and cached. Subsequent runs will be faster. Pre-download models offline if needed.

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
```

### Environment Variables

```bash
FLASK_ENV=production
DEBUG=False
PORT=5000
```

See **DEPLOYMENT.md** for detailed cloud deployment instructions.

---

## 👥 Contributors

- **Ashutosh Behera** ([@ASHUTOSH-A-49](https://github.com/ASHUTOSH-A-49)) - Backend & Architecture
- **Rahul Sahu** ([@Rahulsahu7389](https://github.com/Rahulsahu7389)) - Frontend & UI

Made with ❤️ by **Bit_Masters** during **CU9.0 2025**

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🔗 Resources

- [Faster-Whisper Documentation](https://github.com/SYSTRAN/faster-whisper)
- [Meta NLLB Model](https://ai.facebook.com/research/nllb/)
- [Flask-SocketIO Guide](https://python-socketio.readthedocs.io/)
- [React Socket.IO Client](https://socket.io/docs/v4/client-api/)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.

---

## 🎯 Future Enhancements

- [ ] Support for video file processing
- [ ] Speaker identification & diarization
- [ ] Sentiment analysis on captions
- [ ] Custom vocabulary/domain-specific terms
- [ ] Real-time collaboration for group captions
- [ ] Mobile app (React Native)
- [ ] Offline mode with cached models
- [ ] Custom model fine-tuning interface

---

**Built with** 🧠 **AI**, ⚡ **WebSockets**, and 🎨 **Modern Web Tech**
