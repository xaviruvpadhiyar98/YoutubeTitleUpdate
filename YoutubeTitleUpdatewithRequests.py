from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from time import sleep


from requests import get

def FindViewsandLikeCount():
	try:
		sourceCode = get("https://www.youtube.com/watch?v=6VU0h-pfibQ")
		index = 0
		for index,x in enumerate(sourceCode.text.split()):
			if "watch7-views-info" in x:
				break
		viewCount = sourceCode.text.split()[index+1].split(">")[1]
		index = 0
		for index,x in enumerate(sourceCode.text.split()):
			if "likeCountText" in x:
				likeCount = x
				break
		for index,x in enumerate(likeCount.split("\\")):
			if "likeCount" in x:
				break
		likeCount = likeCount.split("\\")[index+1].split(":")[-1].replace(",","")
		return int(viewCount), int(likeCount)
	except:
		print("Something went wrong!.")


CLIENT_SECRETS_FILE = 'ClientSecretS.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
youtubeId = "6VU0h-pfibQ"

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

viewCount = 0
likeCount = 0
counter = 0

while True:
	try:
		curentviewCount, currentlikeCount = FindViewsandLikeCount()
		if curentviewCount > viewCount or currentlikeCount > likeCount:
			viewCount = curentviewCount
			likeCount = currentlikeCount
			Updatetitle = f"This Video has {viewCount} views and {likeCount} likes."
			videos_list_snippet = {'publishedAt': '2020-05-25T09:40:58Z', 'channelId': 'UCxqQq91PUgR7RqseFpkSMLw', 'title': 'This Video has 139 views, 17 comments and 12 likes.', 'description': '**So I have Exhausted the daily Quota and this wont work now! ** Apologies.\n\n\nThis video will update the title automatically according to views, comments and likes.\nSubscribe to see the tutorial for the following video.\n\nThank You for watching...\nCode will be updated on GitHub soon.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/hqdefault.jpg', 'width': 480, 'height': 360}, 'standard': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/sddefault.jpg', 'width': 640, 'height': 480}, 'maxres': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/maxresdefault.jpg', 'width': 1280, 'height': 720}}, 'channelTitle': 'Dhruv Padhiyar', 'categoryId': '28', 'liveBroadcastContent': 'none', 'localized': {'title': 'This Video has 139 views, 17 comments and 12 likes.', 'description': '**So I have Exhausted the daily Quota and this wont work now! ** Apologies.\n\n\nThis video will update the title automatically according to views, comments and likes.\nSubscribe to see the tutorial for the following video.\n\nThank You for watching...\nCode will be updated on GitHub soon.'}, 'defaultAudioLanguage': 'en-US'}
			videos_list_snippet['title'] = Updatetitle
			videos_update_response = youtube.videos().update(part='snippet',body=dict(snippet=videos_list_snippet,id=youtubeId)).execute()
			print("Video has been updated")
		counter += 1
		if counter % 100 == 0:
			print(f"Completed {counter} iterations")
	except:
		print("Something Went Wrong! We will fix it soon")	
	sleep(10)
	
	
'''	
print(videos_list_response)


{'kind': 'youtube#videoListResponse', 'etag': 'wgeljDeol9fOnbp7T9ZYnR5lWOQ', 'items': [{'kind': 'youtube#video', 'etag': 'I8vRwBBNjqy9brjBghzKqwArxOs', 'id': '6VU0h-pfibQ', 'snippet': {'publishedAt': '2020-05-25T09:40:58Z', 'channelId': 'UCxqQq91PUgR7RqseFpkSMLw', 'title': 'This Video has 139 views, 17 comments and 12 likes.', 'description': '**So I have Exhausted the daily Quota and this wont work now! ** Apologies.\n\n\nThis video will update the title automatically according to views, comments and likes.\nSubscribe to see the tutorial for the following video.\n\nThank You for watching...\nCode will be updated on GitHub soon.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/hqdefault.jpg', 'width': 480, 'height': 360}, 'standard': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/sddefault.jpg', 'width': 640, 'height': 480}, 'maxres': {'url': 'https://i.ytimg.com/vi/6VU0h-pfibQ/maxresdefault.jpg', 'width': 1280, 'height': 720}}, 'channelTitle': 'Dhruv Padhiyar', 'categoryId': '28', 'liveBroadcastContent': 'none', 'localized': {'title': 'This Video has 139 views, 17 comments and 12 likes.', 'description': '**So I have Exhausted the daily Quota and this wont work now! ** Apologies.\n\n\nThis video will update the title automatically according to views, comments and likes.\nSubscribe to see the tutorial for the following video.\n\nThank You for watching...\nCode will be updated on GitHub soon.'}, 'defaultAudioLanguage': 'en-US'}}], 'pageInfo': {'totalResults': 1, 'resultsPerPage': 1}}



'''



	
	

