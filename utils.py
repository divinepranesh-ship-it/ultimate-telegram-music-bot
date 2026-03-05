import yt_dlp

def download_audio(url):

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
