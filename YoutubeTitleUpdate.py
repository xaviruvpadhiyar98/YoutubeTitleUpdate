from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from time import sleep

CLIENT_SECRETS_FILE = 'ClientSecretS.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
youtubeId = "6VU0h-pfibQ"

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

viewCount = 0
commentCount = 0
likeCount = 0
counter = 0

while True:
	videos_list_response = youtube.videos().list(id=youtubeId,part='snippet, statistics').execute()
	if videos_list_response["items"][0]["statistics"]["viewCount"] > viewCount or videos_list_response["items"][0]["statistics"]["commentCount"] > commentCount or videos_list_response["items"][0]["statistics"]["likeCount"] > likeCount:
		viewCount = videos_list_response["items"][0]["statistics"]["viewCount"]
		commentCount = videos_list_response["items"][0]["statistics"]["commentCount"]
		likeCount = videos_list_response["items"][0]["statistics"]["likeCount"]	
		Updatetitle = f"This Video has {viewCount} views, {commentCount} comments and {likeCount} likes."
		videos_list_snippet = videos_list_response['items'][0]['snippet']
		videos_list_snippet['title'] = Updatetitle
		videos_update_response = youtube.videos().update(part='snippet',body=dict(snippet=videos_list_snippet,id=youtubeId)).execute()
		print("Video has been updated")
	counter += 1
	if counter % 100 :
		print(f"Completed {counter} iterations")
		
	sleep(10)
	




