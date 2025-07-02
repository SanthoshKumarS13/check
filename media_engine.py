# media_engine.py
import requests
import os
import random
from config import PEXELS_API_KEY, JAMENDO_CLIENT_ID

class MediaFetcher:
    def __init__(self):
        os.makedirs("temp_media", exist_ok=True)
        os.makedirs("audio", exist_ok=True) # <-- CHANGED

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
        if not PEXELS_API_KEY:
            print("   - PEXELS_API_KEY not found. Skipping video fetch.")
            return None, None
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": query, "per_page": 15, "orientation": "portrait"}
        try:
            res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
            res.raise_for_status()
            videos = res.json().get('videos', [])
            if not videos:
                print(f"   - No videos found for query '{query}', trying fallback 'abstract technology'.")
                if query == "abstract technology": return None, None # Prevent infinite recursion
                return self.get_video("abstract technology")

            video = random.choice(videos)
            video_url = random.choice(video['video_files'])['link']
            credit = video['user']['name']
            filename = f"pexels_{video['id']}.mp4"
            
            return self._download_file(video_url, filename), credit
        except Exception as e:
            print(f"Error fetching video from Pexels: {e}")
            return None, None

    def _get_local_music(self):
        """Picks a random music file from the local 'audio' directory as a fallback."""
        print("   - Attempting to fetch music from local 'audio' folder...")
        try:
            music_files = [f for f in os.listdir("audio") if f.endswith((".mp3", ".wav"))] # <-- CHANGED
            if not music_files:
                print("   -> Error: The 'audio' folder is empty. No fallback music available.")
                return None, None
            
            chosen_song = random.choice(music_files)
            print(f"   - Selected local music: {chosen_song}")
            return os.path.join("audio", chosen_song), os.path.splitext(chosen_song)[0] # <-- CHANGED
        except Exception as e:
            print(f"Error reading from local audio folder: {e}")
            return None, None
            
    def _get_jamendo_music(self):
        """Fetches music from the Jamendo API."""
        if not JAMENDO_CLIENT_ID: return None, None
        print("   - Attempting to fetch music from Jamendo API...")
        try:
            params = {
                "client_id": JAMENDO_CLIENT_ID,
                "format": "json",
                "limit": 50,
                "tags": "electronic,ambient,tech,corporate,future",
                "order": "popularity_month"
            }
            res = requests.get("https://api.jamendo.com/v3.0/tracks/", params=params, timeout=10)
            res.raise_for_status()
            tracks = res.json().get('results', [])
            if not tracks: return None, None

            track = random.choice(tracks)
            music_url = track.get('audio', '')
            credit = track.get('artist_name', 'Jamendo Artist')
            filename = f"jamendo_{track['id']}.mp3"

            return self._download_file(music_url, filename), credit
        except Exception as e:
            print(f"   -> Error fetching music from Jamendo: {e}")
            return None, None

    def get_music(self, query=None):
        """Tries Jamendo API first, then falls back to the local folder."""
        # Step 1: Try Jamendo API
        music_path, credit = self._get_jamendo_music()
        if music_path:
            return music_path, credit

        # Step 2: Fallback to Local Folder
        print("-> Jamendo API failed or returned no results. Falling back to local music folder.")
        return self._get_local_music()
