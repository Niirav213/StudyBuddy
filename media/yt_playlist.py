from re import sub
import subprocess
import json
from pathlib import Path


curr_dir = Path(__file__).parent
json_file_path = curr_dir / "cache" / "playlist_cache.jsonl"
json_file_path.parent.mkdir(parents=True, exist_ok=True)

def fetch_playlist(playlist_url: str) -> list[dict]:

    command = ['yt-dlp', '--dump-json', '--flat-playlist', playlist_url]
    try:

        process = subprocess.Popen(command, stdout= subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print("yt-dlp is not installed\n install it from github")
        return []
    videos = []

    for line in process.stdout:
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
            videos.append({
                "id" : data.get("id"),
                "title": data.get("title"),
                "duration": data.get("duration")
            })
        except json.JSONDecodeError:
            continue

    process.wait()
    if process.returncode != 0:
        error_message = process.stderr.read().strip()
        raise RuntimeError(f"yt-dlp failed with error {error_message}")
    return videos



def save_cache(videos: list[dict]) -> None:


    json_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_file_path, "w", encoding='utf-8') as file:

        file.write(json.dumps(videos))



def load_cache()->list[dict]:
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:

            output = json.load(file)
        return output
    except FileNotFoundError:
        return []


def resolve_stream_urls(video_id: str)-> tuple[str, str]:

    yt_url = f"https://www.youtube.com/watch?v={video_id}"


    command = ['yt-dlp', '--get-url', yt_url]
    try:
        urls = subprocess.run(command, capture_output=True, text=True)
        video_url, audio_url = urls.stdout.strip().split('\n')


    except FileNotFoundError:
        raise RuntimeError("yt-dlp not found — install it first")

    
    return (video_url, audio_url)