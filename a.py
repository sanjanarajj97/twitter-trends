from YT import YTData
import requests, json
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = 'https://www.googleapis.com/youtube/v3/videos'
api_key = 'your YT key'
def collectYTData():
    ytObj = YTData(URL, api_key)
    category_id_map = {
        1: 'Film & Animation',
        2: 'Autos & Vehicles',
        10: 'Music',
        15: 'Pets & Animals',
        17: 'Sports',
        18: 'Short Movies',
        19: 'Travel & Events',
        20: 'Gaming',
        21: 'Videoblogging',
        22: 'People & Blogs',
        23: 'Comedy',
        24: 'Entertainment',
        25: 'News & Politics',
        26: 'Howto & Style',
        27: 'Education',
        28: 'Science & Technology',
        29: 'Nonprofits & Activism',
        30: 'Movies',
        31: 'Anime/Animation',
        32: 'Action/Adventure',
        33: 'Classics',
        34: 'Comedy',
        35: 'Documentary',
        36: 'Drama',
        37: 'Family',
        38: 'Foreign',
        39: 'Horror',
        40: 'Sci-Fi/Fantasy',
        41: 'Thriller',
        42: 'Shorts',
        43: 'Shows',
        44: 'Trailers'
    }
    regions = ['US', 'GB', 'CA', 'IN', 'KR', 'FR', 'GE']
    while(True):
        url = 'https://localhost:9200/youtube/_delete_by_query'
        h = {"Content-Type": "application/json"}
        p_request = {
            "query" : {
                "match_all" : {}
            }
        }
        p_response = requests.post(url, verify=False, headers=h, data=json.dumps(p_request), auth=("elastic", "your_elastic_password"))
        data = p_response.json()
        print('Deleting existing data if any.')
        print(p_response)
        for region in regions:
            videos = ytObj.get_trending_videos(region)
            for video in videos:
                v = {}
                v['title'] = ''
                v['description'] = ''
                v['tags'] = []
                v['category'] = 'Other'
                v['channel'] = ''
                v['blockedRegions'] = []
                v['region'] = region
                if 'snippet' in video:
                    if 'title' in video['snippet']:
                        v['title'] = video['snippet']['title']
                    if 'description' in video['snippet']:
                        v['description'] = video['snippet']['description']
                    if 'tags' in video['snippet']:
                        v['tags'] = video['snippet']['tags']
                    if 'categoryId' in video['snippet'] and int(video['snippet']['categoryId']) in category_id_map:
                        v['category'] = category_id_map[int(video['snippet']['categoryId'])]
                    if 'channelTitle' in video['snippet']:
                        v['channel'] = video['snippet']['channelTitle']
                if('contentDetails' in video and 'regionRestriction' in video['contentDetails'] and 'blocked' in video['contentDetails']['regionRestriction']):
                    v['blockedRegions'] = video['contentDetails']['regionRestriction']['blocked']
                p_data = {
                    "title": v['title'],
                    "description": v['description'],
                    "tags": v['tags'],
                    "category": v['category'],
                    "channel": v['channel'],
                    "blockedRegions": v['blockedRegions'],
                    "region": v['region']
                }
                url = 'https://localhost:9200/youtube/_doc'
                h = {"Content-Type": "application/json"}
                p_response = requests.post(url, verify=False, headers=h, data=json.dumps(p_data), auth=("elastic", "wN5hvPrcCOk6L9G_t0Jy"))
                data = p_response.json()
        print('Database updated with latest trending videos data. Please press enter to refetch the data.')
        print('Press Ctrl-C(^C) to exit.')
        input()


if __name__ == '__main__':
    collectYTData()