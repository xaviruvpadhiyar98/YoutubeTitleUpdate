import json
import re
from time import sleep

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def generate_meta_data_from_url(url: str) -> dict:
    """
    Generates meta data from a given url using YoutubeDL from yt_dlp.

    Args:
        url (str): The url of the video.

    Returns:
        dict: The meta data of the video.
    """
    with YoutubeDL({"verbose": False, "logger": False, "quiet": True}) as ydl:
        return ydl.extract_info(
            url,
            download=False,
            process=False,
        )


def check_title_matches_viewLikeCount(
    title: str,
    viewCount: int,
    likeCount: int,
) -> bool:
    """
    Checks if the title of a video matches the view count and like count.

    Args:
        title (str): The title of the video.
        viewCount (int): The view count of the video.
        likeCount (int): The like count of the video.

    Returns:
        bool: True if the title matches the view count and like count, else False
    """
    titleViewCount = re.search(r"has (.*?) views", title).group(1)
    titleLikeCount = re.search(r"and (.*?) likes", title).group(1)

    if titleViewCount == str(viewCount) and titleLikeCount == str(likeCount):
        return True
    return False


def update_title(viewCount: int, likeCount: int) -> dict:
    """
    Updates the title of a video.

    Args:
        viewCount (int): The view count of the video.
        likeCount (int): The like count of the video.

    Returns:
        dict: The Response of the update operation on video.
    """

    with open("video_snippet.json", "r", encoding="utf-8") as f:
        video_snippet = json.load(f)

    video_snippet["title"] = f"This Video has {viewCount} views and {likeCount} likes."
    videos_update_response = (
        youtube.videos()
        .update(part="snippet", body={"snippet": video_snippet, "id": YOUTUBEID})
        .execute()
    )
    return videos_update_response


def main():
    while True:
        try:
            meta_data = generate_meta_data_from_url(YOUTUBEURL)
            title = meta_data.get("title", None)
            viewCount = meta_data.get("view_count", None)
            likeCount = meta_data.get("like_count", None)
            if check_title_matches_viewLikeCount(title, viewCount, likeCount):
                print("Title matches view count and like count. No update needed.")
            else:
                print("Updating title...")
                youtube_update_title_response = update_title(viewCount, likeCount)
                if youtube_update_title_response.get("title", None):
                    print("Title updated successfully.")
                else:
                    print("Title update failed.")
        except Exception as e:
            print("Something Went Wrong! We will fix it soon")
            print(e)

        print("Sleeping for 10 minutes...")
        sleep(60 * 10)


if __name__ == "__main__":

    YOUTUBEID = "6VU0h-pfibQ"
    YOUTUBEURL = "https://www.youtube.com/watch?v=6VU0h-pfibQ"
    main()
