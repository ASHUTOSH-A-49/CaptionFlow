import whisper

class SpeechToText:
    """OpenAI Whisper - FREE Speech-to-Text"""
    
    def __init__(self, language_code='hi'):
        self.language_code = language_code
        print(f"📍 Loading Whisper model...")
        try:
            self.model = whisper.load_model('base')
            print(f"✅ Whisper loaded!")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.model = None
    
    def transcribe_audio_file(self, audio_file_path):
        """Transcribe audio file - FORCE language"""
        try:
            if not self.model:
                return {'transcript': '', 'confidence': 0}
            
            print(f"🎙️ Transcribing in {self.language_code}...")
            result = self.model.transcribe(
                audio_file_path,
                language=self.language_code,
                task='transcribe',
                verbose=False,
                fp16=False  # ADD THIS - helps with stability
            )
            
            transcript = result['text'].strip()
            print(f"✅ Got: {transcript[:50]}...")
            
            return {
                'transcript': transcript,
                'confidence': 0.95
            }
        except Exception as e:
            print(f"❌ Error: {e}")
            return {'transcript': '', 'confidence': 0}
