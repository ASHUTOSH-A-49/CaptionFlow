# local_stt_service.py
import os
import logging
import requests

logger = logging.getLogger(__name__)

class SarvamSTTService:
    def __init__(self):
        self.api_key = os.getenv('SARVAM_API_KEY')
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY missing")
        self.headers = {
            'api-subscription-key': self.api_key,
            'Accept': 'application/json'
        }
        self.speech_to_text_url = "https://api.sarvam.ai/speech-to-text"
        self.translate_url = "https://api.sarvam.ai/translate"

    def transcribe_audio(self, audio_bytes, language_code):
        # HTTP POST to Sarvam speech-to-text endpoint
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"language_code": language_code, "model": "saarika:v2"}
        response = requests.post(self.speech_to_text_url, headers=self.headers, files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Sarvam STT API error: {response.status_code} - {response.text}")
            return None

    def translate_text(self, text, target_lang, source_lang="en-IN"):
        payload = {
            "input": text,
            "source_language_code": source_lang,
            "target_language_code": target_lang,
            "model": "mayura:v1",
            "mode": "formal"
        }
        response = requests.post(self.translate_url, headers=self.headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("translated_text", text)
        else:
            logger.error(f"Sarvam translation API error: {response.status_code}")
            return text
