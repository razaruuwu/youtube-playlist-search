from googleapiclient.discovery import build

api_key = 'your api key'
def f(playlistId):
    youtube = build('youtube', 'v3', developerKey=api_key)

    res = youtube.playlistItems().list(part='snippet', playlistId=playlistId, maxResults="50").execute()

    return res

