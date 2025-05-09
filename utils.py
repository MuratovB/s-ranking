import os, requests
from random import shuffle
from dotenv import load_dotenv

load_dotenv()

def fetch_videos(playlist_id):
    api_key = os.getenv("YOUTUBE_API")

    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    videos = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "pageToken": next_page_token,
            "key": api_key,
        }

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch videos: {response.text}")

        data = response.json()
        videos.extend(data.get("items", []))
        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

    for i, video in enumerate(videos):
        # Extract title, videoId, high res thumbnail
        video_id = video["snippet"]["resourceId"]["videoId"]
        title = video["snippet"]["title"]
        thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]
        videos[i] = {
            "videoId": video_id,
            "title": title,
            "thumbnail_url": thumbnail_url,
        }

    if len(videos) <= 1:
        raise Exception("Not enough videos in the playlist.")

    videos = [videos]

    shuffle(videos)

    return videos

async def send_message_to_model(message):
    api_key = os.getenv("NLP_MODEL_API")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [{"text": message}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        result_text = data['candidates'][0]['content']['parts'][0]['text']
        print(result_text)
        return result_text
    except requests.RequestException as e:
        print("Error:", e)
        return None
