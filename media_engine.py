# media_engine.py
import requests
import os
import random
from config import PEXELS_API_KEY, PIXABAY_API_KEY

class MediaFetcher:
    def __init__(self):
        os.makedirs("temp_media", exist_ok=True)

    def _download_file(self, url, filename):
        try:
            path = os.path.join("temp_media", filename)
            if os.path.exists(path):
                print(f"   - Using cached media: {filename}")
                return path
                
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"   - Downloaded media: {filename}")
            return path
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return None

    def get_video(self, query):
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": query, "per_page": 10, "orientation": "portrait"}
        try:
            res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
            res.raise_for_status()
            videos = res.json().get('videos', [])
            if not videos: return None, None
            
            video = random.choice(videos)
            video_url = random.choice(video['video_files'])['link']
            credit = video['user']['name']
            filename = f"{video['id']}.mp4"
            
            return self._download_file(video_url, filename), credit
        except Exception as e:
            print(f"Error fetching video from Pexels: {e}")
            return None, None

    def get_music(self, query):
        params = {"key": PIXABAY_API_KEY, "q": query, "per_page": 10}
        try:
            res = requests.get("https://pixabay.com/api/music/", params=params)
            res.raise_for_status()
            tracks = res.json().get('hits', [])
            if not tracks: return self.get_music("background instrumental")
            
            track = random.choice(tracks)
            music_url = track['downloadURL']
            credit = track['user']['name']
            filename = f"{track['id']}.mp3"

            return self._download_file(music_url, filename), credit
        except Exception as e:
            print(f"Error fetching music from Pixabay: {e}")
            return None, None