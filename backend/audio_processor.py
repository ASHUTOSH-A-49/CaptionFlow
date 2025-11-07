import os
import subprocess

class AudioProcessor:
    """Extract audio from video using ffmpeg only (NO pydub)"""
    
    @staticmethod
    def extract_audio_from_video(video_path, output_path="temp_audio.wav"):
        """Extract audio from video file using ffmpeg"""
        try:
            print(f"📍 Extracting audio from: {video_path}")
            
            command = [
                'ffmpeg',
                '-i', video_path,
                '-ar', '16000',          # Sample rate: 16kHz
                '-ac', '1',              # Mono
                '-f', 'wav',
                output_path,
                '-y'                     # Overwrite
            ]
            
            subprocess.run(command, check=True, capture_output=True)
            print(f"✅ Audio extracted: {output_path}")
            return output_path
        
        except FileNotFoundError:
            print("❌ FFmpeg not found! Install: choco install ffmpeg")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None