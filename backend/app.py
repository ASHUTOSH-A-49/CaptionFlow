import sounddevice as sd
import numpy as np
import queue
import threading
from flask import Flask
from flask_socketio import SocketIO, emit
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Flask app and socket setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Audio and Whisper configuration
samplerate = 16000
block_duration = 0.5
chunk_duration = 2
frames_per_block = int(samplerate * block_duration)
frames_per_chunk = int(samplerate * chunk_duration)
channels = 1

# Audio buffers
audio_queue = queue.Queue()
audio_buffer = []

# Global control flags
recorder_thread = None
transcriber_thread = None
listening = False
target_lang = "bho_Deva"  # Default

# Load Whisper model (faster-whisper)
whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

# Load NLLB model
print("Loading translation model...")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
translator_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
translator = pipeline("translation", model=translator_model, tokenizer=tokenizer,
                      src_lang="eng_Latn", tgt_lang=target_lang, device=-1)
print("Translation model ready.")

def audio_callback(indata, frames, time, status):
    if status:
        print("Mic error:", status)
    audio_queue.put(indata.copy())

def recorder():
    global listening
    with sd.InputStream(samplerate=samplerate, channels=channels,
                        blocksize=frames_per_block, callback=audio_callback):
        print("🎙️ Listening...")
        while listening:
            sd.sleep(100)

def transcriber():
    global audio_buffer
    while listening:
        block = audio_queue.get()
        audio_buffer.append(block)

        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frames_per_chunk:
            audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            audio_buffer = []

            audio_data = audio_data.flatten().astype(np.float32)

            segments, _ = whisper_model.transcribe(audio_data, language="en", beam_size=5)
            for segment in segments:
                original = segment.text.strip()
                if not original:
                    continue

                result = translator(original, tgt_lang=target_lang)
                translated = result[0]['translation_text']

                print("➡️", original)
                print("🌍", translated)

                socketio.emit("translated_text", {
                    "original": original,
                    "translated": translated
                })

@app.route("/")
def index():
    return "Flask backend running."

@socketio.on("start_transcription")
def handle_start(data):
    global recorder_thread, transcriber_thread, listening, target_lang
    if listening:
        print("Already listening...")
        return
    target_lang = data.get("target_lang", "bho_Deva")
    listening = True
    recorder_thread = threading.Thread(target=recorder)
    transcriber_thread = threading.Thread(target=transcriber)
    recorder_thread.start()
    transcriber_thread.start()
    print(f"🟢 Started listening. Target: {target_lang}")

@socketio.on("stop_transcription")
def handle_stop():
    global listening
    listening = False
    print("🔴 Stopped listening.")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)