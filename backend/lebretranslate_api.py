import requests

class LibreTranslator:
    def __init__(self, base_url="https://libretranslate.de/translate"):
        self.base_url = base_url  # Can also self-host your own server
    
    def translate_text(self, text, source_lang="en", target_lang="hi"):
        payload = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }
        response = requests.post(self.base_url, data=payload)
        if response.status_code == 200:
            return response.json().get("translatedText", "")
        else:
            raise Exception(f"LibreTranslate Error {response.status_code}: {response.text}")