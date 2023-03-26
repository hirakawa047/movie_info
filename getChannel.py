# https://su-gi-rx.com/archives/4528

import pandas as pd
from apiclient.discovery import build
from apiclient.errors import HttpError
import re

API_KEY = 'AIzaSyCMi3RXxT9RTLK4JnGfn8hRZiXQZ1MIqXE' #取得したAPIキー
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
#CHANNEL_ID = 'UCpoPaQt8v-_72nDqUbtVO1g'
CHANNEL_ID = 'UCHBqTYEwBSR1h6zGmHdue7g'
#CHANNEL_ID = 'UCHuEAf_vytSUkliGEyLlQPg'
channels = [] #チャンネル情報を格納する配列
searches = [] #videoidを格納する配列
videos = [] #各動画情報を格納する配列
nextPagetoken = None
nextpagetoken = None

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey = API_KEY
)


# Get movie list
'''
search_response = youtube.search().list(
part='snippet',
#検索したい文字列を指定
q='ボードゲーム',
#視聴回数が多い順に取得
order='viewCount',
type='video',
).execute()

print(search_response['items'][0])

'''

channel_response = youtube.channels().list(
part = 'snippet,statistics',
id  = CHANNEL_ID,
).execute()

for channel_result in channel_response.get("items", []):
    if channel_result["kind"] == "youtube#channel":
        channels.append([channel_result["snippet"]["title"],channel_result["statistics"]["subscriberCount"],channel_result["statistics"]["videoCount"],channel_result["snippet"]["publishedAt"]])

while True:
    if nextPagetoken != None:
        nextpagetoken = nextPagetoken

    search_response = youtube.search().list(
      part = "snippet",
      channelId = CHANNEL_ID,
      maxResults = 50,
      order = "date", #日付順にソート
      pageToken = nextpagetoken #再帰的に指定
      ).execute()
 
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            searches.append(search_result["id"]["videoId"])

    try:
        nextPagetoken =  search_response["nextPageToken"]
    except:
        break

'''
for result in searches:
    video_response = youtube.videos().list(
      part = 'snippet,statistics',
      id = result
      ).execute()

    for video_result in video_response.get("items", []):
        if video_result["kind"] == "youtube#video":
            videos.append([video_result["snippet"]["title"],video_result["snippet"]["description"],video_result["statistics"]["viewCount"],video_result["statistics"]["likeCount"],video_result["statistics"]["commentCount"],video_result["snippet"]["publishedAt"],video_result["id"]])
'''        

pat = r'(\r?\n)|(\r\n?)'

for result in searches:
    video_response = youtube.videos().list(
      part = 'snippet,statistics',
      id = result
      ).execute()

    for video_result in video_response.get("items", []):
        if video_result["kind"] == "youtube#video":
            videos.append([video_result["snippet"]["title"],re.sub(pat, '""', video_result["snippet"]["description"]),video_result["statistics"]["viewCount"],video_result["statistics"]["likeCount"],video_result["snippet"]["publishedAt"],video_result["id"]])
        

videos_report = pd.DataFrame(videos, columns=['title','Description', 'viewCount', 'likeCount', 'publishedAt', 'vidoId'])
#videos_report.to_csv("videos_report.csv", index=None)
output_file_neme = "raw_data_" + CHANNEL_ID + ".csv"
videos_report.to_csv(open(output_file_neme, 'w', newline='', encoding='utf_8_sig'))

channel_report = pd.DataFrame(channels, columns=['title', 'subscriberCount', 'videoCount', 'publishedAt'])
#channel_report.to_csv("channels_report.csv", index=None)