# Script fot getting video list from youtube
# Reference : https://qiita.com/g-k/items/7c98efe21257afac70e9


from apiclient.discovery import build
import pandas as pd

YOUTUBE_API_KEY = 'AIzaSyCMi3RXxT9RTLK4JnGfn8hRZiXQZ1MIqXE'

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

'''
search_response = youtube.search().list(
part='snippet',
#検索したい文字列を指定
q='aaa',
#視聴回数が多い順に取得
order='viewCount',
type='video',
).execute()
'''


def get_video_info(part, q, order, type, num):
    dic_list = []
    search_response = youtube.search().list(part=part,q=q,order=order,type=type)
    output = youtube.search().list(part=part,q=q,order=order,type=type).execute()

    #一度に5件しか取得できないため何度も繰り返して実行
    for i in range(num):        
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()

    df = pd.DataFrame(dic_list)
    #各動画毎に一意のvideoIdを取得
    df1 = pd.DataFrame(list(df['id']))['videoId']
    #各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','publishedAt','channelId','title','description']]
    ddf = pd.concat([df1,df2], axis = 1)

    return ddf

def get_statistics(id):
    statistics = youtube.videos().list(part = 'statistics', id = id).execute()['items'][0]['statistics']
    return statistics


# Gen movie list in sprcified playlist
def get_video_id_in_playlist(playlistId):
    video_id_list = []

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlistId,
        fields="nextPageToken,items/snippet/resourceId/videoId"
    )

    while request:
        response = request.execute()
        video_id_list.extend(list(map(lambda item: item["snippet"]["resourceId"]["videoId"], response["items"])))
        request = youtube.playlistItems().list_next(request, response)

    return video_id_list

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Get video iformation
def get_video_items(video_id_list):
    video_items = []

    chunk_list = list(chunks(video_id_list, 50)) # max 50 id per request.
    for chunk in chunk_list:
        video_ids = ",".join(chunk)
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_ids,
            fields="items(id,snippet(title,description,publishedAt,thumbnails),statistics(viewCount,likeCount))"
        )
        response = request.execute()
        video_items.extend(response["items"])

    return video_items

def get_image_url(video_item):
    qualities = ['standard', 'high', 'medium', 'default']
    for quality in qualities:
        if quality in video_item['snippet']['thumbnails'].keys():
            return video_item['snippet']['thumbnails'][quality]['url']
    return ''


def convertVideoItems(video_items):
    return list(map(lambda item: {
        'id': item["id"],
        'title': item["snippet"]["title"],
        'publishedAt': item["snippet"]["publishedAt"],
        'views': int(item["statistics"]["viewCount"]) if 'viewCount' in item["statistics"].keys() else 0,
        'likes': int(item["statistics"]["likeCount"]) if 'likeCount' in item["statistics"].keys() else 0,
        'image': get_image_url(item),
    }, video_items))

df = get_video_info(part='snippet',q='ワンピース',order='viewCount',type='video',num = 4)

df_static = pd.DataFrame(list(df['videoId'].apply(lambda x : get_statistics(x))))

df_output = pd.concat([df,df_static], axis = 1)

df_output['viewCount'] = df_output['viewCount'].astype(int) 
#list = get_video_info(part='snippet',q='ワンピース',order='viewCount',type='video',num = 20)

print(df_output)

df_output.groupby('channelTitle').sum().sort_values(by = 'viewCount', ascending = False).plot( kind='bar', y = 'viewCount', figsize = (25,10), fontsize = 20)