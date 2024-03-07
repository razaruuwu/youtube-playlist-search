from googleapiclient.discovery import build
from os import mkdir

api_key = input('input your api key: ')
playlist_id = input('input playlist url: ')
playlist_id = playlist_id.replace('https://www.youtube.com/playlist?list=', '')

try:
    mkdir('files')
except:
    pass

def fetch(playlistId):
    youtube = build('youtube', 'v3', developerKey=api_key)

    res = youtube.playlistItems().list(part="snippet", playlistId=playlistId, maxResults="50").execute()

    next_page_token = res.get('nextPageToken')

    while 'nextPageToken' in res:
        nextPage = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlistId,
            maxResults="50",
            pageToken=next_page_token
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            next_page_token = nextPage['nextPageToken']

    return res

m = fetch(playlist_id)

youtube = build('youtube', 'v3', developerKey=api_key)
playlist_name = youtube.playlists().list(part="snippet", id=playlist_id, maxResults="50").execute()['items'][0]['snippet']['localized']['title']

with open(f'files/{playlist_name} - playlist dump.txt', 'w+', encoding='utf-8') as f:
    for i in range(len(m['items'])):
        f.write('{\n')
        try:
            f.write(
                f"number: {i + 1}\ntitle: {m['items'][i]['snippet']['title']}\nchannel: {m['items'][i]['snippet']['videoOwnerChannelTitle']}\n")
            f.write(f"link: https://www.youtube.com/watch?v={m['items'][i]['snippet']['resourceId']['videoId']}\n")
            f.write(f"description: {m['items'][i]['snippet']['description']}\n")
        except:
            f.write(f'number: {i + 1}\n')
            f.write('DELETED VIDEO\n')
        f.write('}\n\n')