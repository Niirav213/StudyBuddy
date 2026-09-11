from base64 import encode
from encodings import utf_16
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



    with open(json_file_path, "a", encoding='utf-8') as file:

        file.write(json.dump(videos) + '\n')



def load_cache()->list[dict]:
    output = []
    with open(json_file_path, 'r', encoding='utf-8') as file:

        for line in file:
            clean_line = line.strip()

            if clean_line:
                data_row = json.load(clean_line)
                output.append(data_row)
