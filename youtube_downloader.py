from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
import os
import re
import sys
import socket
from tqdm import tqdm

# タイムアウト設定（秒）
socket.setdefaulttimeout(30)

# 進捗バーの初期化
progress_bar = None

# YouTube動画をダウンロードする関数
def download_youtube_video(url, file_type='video'):
    """
    YouTubeの動画や音声をダウンロードする関数
    :param url: YouTube動画のURL
    :param file_type: 'video'（動画）または 'audio'（音声）
    """
    global progress_bar
    try:
        # YouTubeオブジェクトを作成
        yt = YouTube(url, on_progress_callback=progress_function, on_complete_callback=complete_function)
        
        # タイトルを取得（安全処理）
        safe_title = re.sub(r'[\/:*?"<>|]', '_', yt.title) if yt.title else "Unknown_Title"
        print(f"Title: {safe_title}")  # 動画タイトル
        print(f"Author: {yt.author}")  # 作者名

        # 保存フォルダの作成
        output_folder = "./downloads"
        os.makedirs(output_folder, exist_ok=True)

        # ダウンロードするストリームを選択
        if file_type == 'video':
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        elif file_type == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            print("Invalid file type. Choose 'video' or 'audio'.")
            return

        if not stream:
            print("No suitable stream found.")
            return

        # 進捗バーの初期化
        progress_bar = tqdm(total=stream.filesize, unit="B", unit_scale=True, desc="Downloading")

        # ダウンロード実行
        print(f"Downloading {file_type}...")
        file_path = os.path.join(output_folder, stream.default_filename)
        stream.download(output_path=output_folder)

    except VideoUnavailable:
        print("\nError: This video is unavailable.")
    except RegexMatchError:
        print("\nError: Invalid YouTube URL.")
    except socket.timeout:
        print("\nError: Network timeout. Please check your connection.")
    except KeyboardInterrupt:
        print("\nDownload canceled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

# ダウンロードの進捗状況を表示する関数
def progress_function(stream, chunk, bytes_remaining):
    global progress_bar
    if progress_bar:
        progress_bar.update(len(chunk))

# ダウンロード完了時の関数
def complete_function(stream, file_path):
    global progress_bar
    if progress_bar:
        progress_bar.close()
    print(f"\nDownload complete! Saved to {file_path}")

# メイン処理
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ").strip()
    file_type = input("Enter file type ('video' or 'audio'): ").strip().lower()
    
    # 動画または音声をダウンロード
    download_youtube_video(video_url, file_type)
