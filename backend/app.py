#---------------------------VERSION 5.0(LATEST)--------------------
# import os
# import threading
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_socketio import SocketIO, emit

# from config import config
# from audio_processor import AudioProcessor
# from speech_to_text import SpeechToText
# from nlp_simplifier import TextSimplifier
# from youtube_handler import YouTubeHandler
# from lebretranslate_api import LibreTranslator

# libre_translator = LibreTranslator()

# app = Flask(__name__)
# # Use a dot to access the attribute
# app.config.from_object(config['development'])

# CORS(app, resources={
#     r"/*": {"origins": "*"}
# })

# socketio = SocketIO(app, cors_allowed_origins="*")

# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# LANGUAGE_CODES = {
#     'en': 'en',
#     'hi': 'hi',
#     'ta': 'ta',
#     'bn': 'bn',
#     'te': 'te',
#     'ml': 'ml',
#     'mr': 'mr',
#     'bho': 'bho',    # Add Bhojpuri here as needed
#     'san': 'san'     # Add Sanskrit here as needed
# }

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file'}), 400

#     file = request.files['file']
#     if not file.filename:
#         return jsonify({'error': 'No file selected'}), 400

#     try:
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         return jsonify({'success': True, 'path': filepath, 'filename': filename}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @socketio.on('connect')
# def on_connect():
#     print(f"Client connected: {request.sid}")
#     emit('connection_response', {'data': 'Connected!'})

# @socketio.on('start_transcription')
# def on_start_transcription(data):
#     video_path = data.get('video_path')
#     lang = data.get('lang', 'en')

#     def transcription_thread(video_path, lang, client_id):
#         try:
#             audio_path = AudioProcessor.extract_audio_from_video(video_path, "temp_audio.wav")
#             if not audio_path:
#                 socketio.emit('error', {'message': 'Failed to extract audio'}, to=client_id)
#                 return

#             language_code = LANGUAGE_CODES.get(lang, 'en')
#             transcriber = SpeechToText(language_code)
#             simplifier = TextSimplifier()

#             result = transcriber.transcribe_audio_file(audio_path)
#             if result.get('transcript'):
#                 simplified = simplifier.simplify_text(result['transcript'])

#                 if lang == 'hi' and language_code == 'en':
#                     translated = libre_translator.translate_text(simplified, source_lang='en', target_lang='hi')
#                 else:
#                     translated = simplified

#                 socketio.emit('caption', {
#                     'text': translated,
#                     'original': result['transcript'],
#                     'confidence': result.get('confidence', 0),
#                 }, to=client_id)

#             socketio.emit('done', {'transcript': result.get('transcript', '')}, to=client_id)

#             if os.path.exists(audio_path):
#                 os.remove(audio_path)

#         except Exception as e:
#             socketio.emit('error', {'message': str(e)}, to=client_id)

#     threading.Thread(target=transcription_thread, args=(video_path, lang, request.sid)).start()

# @socketio.on('process_youtube')
# def on_process_youtube(data):
#     youtube_url = data.get('url')
#     lang = data.get('lang', 'en')

#     def youtube_thread(url, lang, client_id):
#         try:
#             audio_path = YouTubeHandler.download_youtube_audio(url, "temp_youtube.wav")
#             if not audio_path:
#                 socketio.emit('error', {'message': 'Failed to download'}, to=client_id)
#                 return

#             language_code = LANGUAGE_CODES.get(lang, 'en')
#             transcriber = SpeechToText(language_code)
#             simplifier = TextSimplifier()

#             result = transcriber.transcribe_audio_file(audio_path)
#             if result.get('transcript'):
#                 simplified = simplifier.simplify_text(result['transcript'])

#                 if lang == 'hi' and language_code == 'en':
#                     translated = libre_translator.translate_text(simplified, source_lang='en', target_lang='hi')
#                 else:
#                     translated = simplified

#                 socketio.emit('caption', {
#                     'text': translated,
#                     'original': result['transcript'],
#                     'confidence': result.get('confidence', 0),
#                 }, to=client_id)

#             socketio.emit('done', {'transcript': result.get('transcript', '')}, to=client_id)

#             if os.path.exists(audio_path):
#                 os.remove(audio_path)

#         except Exception as e:
#             print(f"Error: {e}")
#             socketio.emit('error', {'message': str(e)}, to=client_id)

#     threading.Thread(target=youtube_thread, args=(youtube_url, lang, request.sid)).start()

# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': '✅ Backend running'}), 200

# if __name__ == '__main__':
#     print("Backend running on http://localhost:5000")
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)


# -------------------------------------VERSION 1.0---------------------------
import sounddevice as sd
import numpy as np
import queue
import threading
from flask import Flask
from flask_socketio import SocketIO, emit
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import time

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

# --multilang-addn---
# Language code mapping: Whisper codes to NLLB codes
LANGUAGE_CODE_MAPPING = {
    "en": "eng_Latn",      # English
    "hi": "hin_Deva",      # Hindi
    "pa": "pan_Guru",      # Punjabi
    "bn": "ben_Beng",      # Bengali
    "ta": "tam_Taml",      # Tamil
    "te": "tel_Telu",      # Telugu
    "mr": "mar_Deva",      # Marathi
    "gu": "guj_Gujr",      # Gujarati
    "kn": "kan_Knda",      # Kannada
    "ml": "mal_Mlym",      # Malayalam
    "ur": "urd_Arab",      # Urdu
    "es": "spa_Latn",      # Spanish
    "fr": "fra_Latn",      # French
    "de": "deu_Latn",      # German
    "zh": "zho_Hans",      # Chinese (Simplified)
    "ja": "jpn_Jpan",      # Japanese
    "ko": "kor_Hang",      # Korean
    "ar": "arb_Arab",      # Arabic
    "ru": "rus_Cyrl",      # Russian
    "pt": "por_Latn",      # Portuguese
}

# ---

# Audio buffers
audio_queue = queue.Queue()
audio_buffer = []

# Global control flags
recorder_thread = None
transcriber_thread = None
listening = False
target_lang = "bho_Deva"  # Default

# ----multi-lang---
detected_lang_code = "en"  # Track detected language
detected_lang_nllb = "eng_Latn"  # NLLB equivalent

# ----

# Load Whisper model (faster-whisper)
# whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
# ---multi-lang-addn---
whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
# -----------


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


# def transcriber():
#     while listening:
#         block = audio_queue.get()
#         audio_data = block.flatten().astype(np.float32)

#         # Use Whisper to transcribe this audio chunk immediately
#         segments, info = whisper_model.transcribe(audio_data, language="en", beam_size=5)

#         detected_lang_code = "en"
#         detected_lang_nllb = "eng_Latn"

#         LANGUAGE_NAMES = {
#             "en": "English",
#             "hi": "Hindi",
#             "pa": "Punjabi",
#             "bn": "Bengali",
#             "ta": "Tamil",
#             "te": "Telugu",
#             "mr": "Marathi",
#             "gu": "Gujarati",
#             "kn": "Kannada",
#             "ml": "Malayalam",
#             "ur": "Urdu",
#             "es": "Spanish",
#             "fr": "French",
#             "de": "German",
#             "zh": "Chinese",
#             "ja": "Japanese",
#             "ko": "Korean",
#             "ar": "Arabic",
#             "ru": "Russian",
#             "pt": "Portuguese",
#             "bho": "Bhojpuri",
#             "san": "Sanskrit"
#         }

#         target_lang_code = target_lang.split("_")[0]
#         lang_name_output = LANGUAGE_NAMES.get(target_lang_code, target_lang_code.upper())
#         lang_name_input = LANGUAGE_NAMES.get(detected_lang_code, "English")

#         for segment in segments:
#             original = segment.text.strip()
#             if not original:
#                 continue

#             try:
#                 from transformers import pipeline
#                 dynamic_translator = pipeline(
#                     "translation",
#                     model=translator_model,
#                     tokenizer=tokenizer,
#                     src_lang=detected_lang_nllb,
#                     tgt_lang=target_lang,
#                     device=-1
#                 )
#                 result = dynamic_translator(original, max_length=400)
#                 translated = result[0]['translation_text']
#             except Exception as e:
#                 print(f"❌ Translation error: {e}")
#                 translated = f"[Translation failed for {detected_lang_code}]"

#             print("➡️", original)
#             print("🌍", translated)

#             socketio.emit("translated_text", {
#                 "original": original,
#                 "translated": translated,
#                 "source_lang": detected_lang_code,
#                 "source_lang_name": lang_name_input,
#                 "target_lang": target_lang,
#                 "target_lang_name": lang_name_output
#             })

# def transcriber():
#     global audio_buffer
#     while listening:
#         block = audio_queue.get()
#         audio_buffer.append(block)

#         total_frames = sum(len(b) for b in audio_buffer)
#         if total_frames >= frames_per_chunk:
#             audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
#             audio_buffer = []

#             audio_data = audio_data.flatten().astype(np.float32)

#             segments, _ = whisper_model.transcribe(audio_data, language="en", beam_size=5)
#             for segment in segments:
#                 original = segment.text.strip()
#                 if not original:
#                     continue

#                 result = translator(original, tgt_lang=target_lang)
#                 translated = result[0]['translation_text']

#                 print("➡️", original)
#                 print("🌍", translated)

#                 socketio.emit("translated_text", {
#                     "original": original,
#                     "translated": translated
#                 })
def transcriber():
    global audio_buffer, detected_lang_code, detected_lang_nllb
    last_clear_time = time.time()
    clear_interval = 5  # seconds to clear buffer
    while listening:
        block = audio_queue.get()
        audio_buffer.append(block)

        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frames_per_chunk:
            audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            audio_buffer = []

            audio_data = audio_data.flatten().astype(np.float32)

            # Always use English as input for tiny.en
            segments, info = whisper_model.transcribe(audio_data, language="en", beam_size=5)

            detected_lang_code = "en"
            detected_lang_nllb = "eng_Latn"

            # Language names for caption
            LANGUAGE_NAMES = {
                "en": "English",
                "hi": "Hindi",
                "pa": "Punjabi",
                "bn": "Bengali",
                "ta": "Tamil",
                "te": "Telugu",
                "mr": "Marathi",
                "gu": "Gujarati",
                "kn": "Kannada",
                "ml": "Malayalam",
                "ur": "Urdu",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "zh": "Chinese",
                "ja": "Japanese",
                "ko": "Korean",
                "ar": "Arabic",
                "ru": "Russian",
                "pt": "Portuguese",
                "bho": "Bhojpuri",
            }

            target_lang_code = target_lang.split("_")[0]
            lang_name_output = LANGUAGE_NAMES.get(target_lang_code, target_lang_code.upper())
            lang_name_input = LANGUAGE_NAMES.get(detected_lang_code, "English")

            for segment in segments:
                original = segment.text.strip()
                if not original:
                    continue

                try:
                    from transformers import pipeline
                    dynamic_translator = pipeline(
                        "translation",
                        model=translator_model,
                        tokenizer=tokenizer,
                        src_lang=detected_lang_nllb,
                        tgt_lang=target_lang,
                        device=-1
                    )
                    result = dynamic_translator(original, max_length=400)
                    translated = result[0]['translation_text']
                except Exception as e:
                    print(f"❌ Translation error: {e}")
                    translated = f"[Translation failed for {detected_lang_code}]"

                print("➡️", original)
                print("🌍", translated)

                # Send captions to frontend
                socketio.emit("translated_text", {
                    "original": original,
                    "translated": translated,
                    "source_lang": detected_lang_code,
                    "source_lang_name": lang_name_input,
                    "target_lang": target_lang,
                    "target_lang_name": lang_name_output
                })
            current_time = time.time()
            if current_time - last_clear_time >= clear_interval:
                audio_buffer = []
                last_clear_time = current_time
                print("♻️ Audio buffer cleared after 10 seconds")



@app.route("/")
def index():
    return "Flask backend running."

# @socketio.on("start_transcription")
# def handle_start(data):
#     global recorder_thread, transcriber_thread, listening, target_lang
#     if listening:
#         print("Already listening...")
#         return
#     target_lang = data.get("target_lang", "bho_Deva")
#     listening = True
#     recorder_thread = threading.Thread(target=recorder)
#     transcriber_thread = threading.Thread(target=transcriber)
#     recorder_thread.start()
#     transcriber_thread.start()
#     print(f"🟢 Started listening. Target: {target_lang}")
@socketio.on("start_transcription")
def handle_start(data):
    global recorder_thread, transcriber_thread, listening, target_lang
    if listening:
        print("Already listening...")
        return
    target_lang = data.get("target_lang", "bho_Deva")
    input_lang_pref = data.get("input_lang", None)  # Optional input language preference
    listening = True
    recorder_thread = threading.Thread(target=recorder)
    transcriber_thread = threading.Thread(target=transcriber)
    recorder_thread.start()
    transcriber_thread.start()
    print(f"🟢 Started listening. Input: Auto-detect | Target: {target_lang}")


@socketio.on("stop_transcription")
def handle_stop():
    global listening
    listening = False
    print("🔴 Stopped listening.")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)


# ---------------------------------------------------------------------


# ----------------------------VERSION 2.0(SARVAM)-----------------------------
# import sounddevice as sd
# import numpy as np
# import queue
# import threading
# from flask import Flask
# from flask_socketio import SocketIO, emit
# from faster_whisper import WhisperModel
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()
# from local_stt_service import SarvamSTTService

# sarvam_service = SarvamSTTService()



# # Load API key from environment for security
# SARVAM_API_ENDPOINT = os.getenv("SARVAM_API_ENDPOINT")
# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
#  # Replace with actual endpoint
# if not SARVAM_API_ENDPOINT:
#     raise Exception("SARVAM_API_ENDPOINT environment variable not set!")

# if not SARVAM_API_KEY:
#     raise Exception("SARVAM_API_KEY environment variable not set!")

# # Flask app and socket setup
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SARVAM_API_KEY', 'your-secret-key-here')
# app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB max
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Audio and Whisper configuration
# samplerate = 16000
# block_duration = 0.5
# chunk_duration = 2
# frames_per_block = int(samplerate * block_duration)
# frames_per_chunk = int(samplerate * chunk_duration)
# channels = 1

# # Language code mapping: Whisper codes to NLLB codes
# LANGUAGE_CODE_MAPPING = {
#     "en": "eng_Latn",     # English
#     "hi": "hin_Deva",     # Hindi
#     "pa": "pan_Guru",     # Punjabi
#     "bn": "ben_Beng",     # Bengali
#     "ta": "tam_Taml",     # Tamil
#     "te": "tel_Telu",     # Telugu
#     "mr": "mar_Deva",     # Marathi
#     "gu": "guj_Gujr",     # Gujarati
#     "kn": "kan_Knda",     # Kannada
#     "ml": "mal_Mlym",     # Malayalam
#     "ur": "urd_Arab",     # Urdu
#     "es": "spa_Latn",     # Spanish
#     "fr": "fra_Latn",     # French
#     "de": "deu_Latn",     # German
#     "zh": "zho_Hans",     # Chinese (Simplified)
#     "ja": "jpn_Jpan",     # Japanese
#     "ko": "kor_Hang",     # Korean
#     "ar": "arb_Arab",     # Arabic
#     "ru": "rus_Cyrl",     # Russian
#     "pt": "por_Latn",     # Portuguese
# }

# # Audio buffers
# audio_queue = queue.Queue()
# audio_buffer = []

# # Global control flags and variables
# recorder_thread = None
# transcriber_thread = None
# listening = False
# target_lang = "bho_Deva"  # Default

# # Load Whisper model (tiny.en for English)
# whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

# # Load NLLB translation model
# print("Loading translation model...")
# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
# translator_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# translator = pipeline("translation", model=translator_model, tokenizer=tokenizer,
#                       src_lang="eng_Latn", tgt_lang=target_lang, device=-1)
# print("Translation model ready.")

# def audio_callback(indata, frames, time, status):
#     if status:
#         print("Mic error:", status)
#     audio_queue.put(indata.copy())

# def recorder():
#     global listening
#     with sd.InputStream(samplerate=samplerate, channels=channels,
#                         blocksize=frames_per_block, callback=audio_callback):
#         print("🎙️ Listening...")
#         while listening:
#             sd.sleep(100)

# def send_to_sarvam(audio_data):
#     import io
#     import wave

#     buffer = io.BytesIO()
#     with wave.open(buffer, 'wb') as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(2)
#         wf.setframerate(samplerate)

#         int_data = np.int16(audio_data * 32767)
#         wf.writeframes(int_data.tobytes())

#     audio_bytes = buffer.getvalue()
#     return sarvam_service.transcribe_audio(audio_bytes, language_code="en-IN")


# def transcriber():
#     global audio_buffer, target_lang, listening

#     while listening:
#         block = audio_queue.get()
#         audio_buffer.append(block)

#         total_frames = sum(len(b) for b in audio_buffer)
#         if total_frames >= frames_per_chunk:
#             audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
#             audio_buffer = []

#             audio_data = audio_data.flatten().astype(np.float32)

#             # Use Sarvam API for English transcription
#             english_text = send_to_sarvam(audio_data)
#             if not english_text:
#                 print("No transcript from Sarvam")
#                 continue

#             print(f"Sarvam transcript: {english_text}")

#             try:
#                 # Translate English to target language using Huggingface pipeline
#                 result = translator(english_text, tgt_lang=target_lang)
#                 translated = result[0]['translation_text']
#             except Exception as e:
#                 print(f"Translation error: {e}")
#                 translated = "[Translation error]"

#             # Emit results to frontend
#             socketio.emit("translated_text", {
#                 "original": english_text,
#                 "translated": translated,
#                 "source_lang": "en",
#                 "source_lang_name": "English",
#                 "target_lang": target_lang,
#                 "target_lang_name": target_lang.split("_")[0].capitalize()
#             })



# @app.route("/")
# def index():
#     return "Flask backend running."

# @socketio.on("start_transcription")
# def handle_start(data):
#     global recorder_thread, transcriber_thread, listening, target_lang, translator

#     if listening:
#         print("Already listening...")
#         return

#     target_lang = data.get("target_lang", "bho_Deva")
    
#     # Update translator pipeline with new target language
#     translator = pipeline(
#         "translation",
#         model=translator_model,
#         tokenizer=tokenizer,
#         src_lang="eng_Latn",
#         tgt_lang=target_lang,
#         device=-1
#     )
    
#     listening = True
#     recorder_thread = threading.Thread(target=recorder)
#     transcriber_thread = threading.Thread(target=transcriber)
#     recorder_thread.start()
#     transcriber_thread.start()
#     print(f"🟢 Started listening. Target: {target_lang}")


# @socketio.on("stop_transcription")
# def handle_stop():
#     global listening
#     listening = False
#     print("🔴 Stopped listening.")

# if __name__ == "__main__":
#     socketio.run(app, host="0.0.0.0", port=5000)

# --------------------------------------------------------------------