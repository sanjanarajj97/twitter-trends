from YT import YTData

URL = 'https://www.googleapis.com/youtube/v3/videos'
api_key = 'AIzaSyCQ0Ui2wVos0r7tRlbnAo1MHvCbXK56gR0'
def collectYTData():
    region = input('Enter region: US, CA, IN, KR\n')
    ytObj = YTData(URL, api_key)
    ytObj.get_trending_videos(region)

if __name__ == '__main__':
    collectYTData()