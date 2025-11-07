class YouTubeHandler:
    """Handle YouTube URLs using yt-dlp"""
    
    @staticmethod
    def get_video_info(youtube_url):
        """Get YouTube video info"""
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                }
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    @staticmethod
    def download_youtube_audio(youtube_url, output_path):
        """Download YouTube audio using yt-dlp"""
        try:
            import yt_dlp
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path.replace('.wav', ''),
                'quiet': False,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"📺 Downloading: {youtube_url}")
                ydl.download([youtube_url])
            
            print(f"✅ Downloaded: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None