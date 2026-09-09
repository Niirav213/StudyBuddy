import subprocess
import json

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
