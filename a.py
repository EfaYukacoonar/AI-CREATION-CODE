from pytube import YouTube

# YouTube動画をダウンロードする関数
def download_youtube_video(url, file_type='video'):
    """
    YouTubeの動画や音声をダウンロードする関数
    :param url: YouTube動画のURL
    :param file_type: 'video'（動画）または 'audio'（音声）
    """
    try:
        # YouTubeオブジェクトを作成
        yt = YouTube(url)
        print(f"Title: {yt.title}")  # 動画タイトル
        print(f"Author: {yt.author}")  # 作者名

        # ダウンロードするストリームを選択
        if file_type == 'video':
            # 動画（音声付き）の最高画質ストリームを選択
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        elif file_type == 'audio':
            # 音声のみのストリームを選択
            stream = yt.streams.filter(only_audio=True).first()
        else:
            print("Invalid file type. Choose 'video' or 'audio'.")
            return

        # ダウンロード実行
        print(f"Downloading {file_type}...")
        stream.download(output_path="./downloads")  # ダウンロード先フォルダ
        print(f"Download complete! Saved to ./downloads/{stream.default_filename}")

    except Exception as e:
        # エラーが発生した場合の処理
        print(f"An error occurred: {e}")


# メイン処理
if __name__ == "__main__":
    # ユーザーからURLを入力
    video_url = input("Enter YouTube video URL: ")
    # ダウンロードタイプ（動画 or 音声）を入力
    file_type = input("Enter file type ('video' or 'audio'): ").strip().lower()

    # 動画または音声をダウンロード
    download_youtube_video(video_url, file_type)
