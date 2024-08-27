import yt_dlp
from concurrent.futures import ThreadPoolExecutor


def download_video(url, output_path='.'):
    try:
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080][ext=mp4]',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Відео успішно завантажене у '{output_path}'")
    except Exception as e:
        print(f"Сталася помилка: {e}")


def download_videos(urls, output_path='.'):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_video, url, output_path) for url in urls]
        for future in futures:
            future.result()


if __name__ == '__main__':
    # Введіть посилання на відео (можна вказати кілька посилань через кому)
    video_urls = input("Введіть URL відео (через кому, якщо декілька): ").split(',')

    # Введіть шлях до папки для збереження
    save_path = input("Введіть шлях до папки для збереження (натисніть Enter для збереження в поточній папці): ")

    # Завантаження відео
    download_videos(video_urls, save_path or '.')
