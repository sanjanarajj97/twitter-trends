from dataclasses import dataclass
import requests
from requests.exceptions import RequestException
from typing import Any, Dict, List

@dataclass
class YTData:
    url: str
    api_key: str

    def getResponse(self, param):
        try:
            res = requests.get(self.url, params=param)
            res.raise_for_status()
        except RequestException:
            print('Error while retrieving: {}'.format(param))
        else:
            return res.json()

    def get_trending_videos(self, region):
        param = {
            'key': self.api_key,
            'chart': 'mostPopular',
            'part': 'snippet,contentDetails,statistics',
            'regionCode': region,
            'maxResults': 10,
        }
        response = self.getResponse(param)
        cursor = response.get('nextPageToken')
        videos = response.get('items')
        while cursor:
            param['pageToken'] = cursor
            response = self.getResponse(param)
            cursor = response.get('nextPageToken')
            videos.extend(response.get('items'))
            print('Got ', len(videos), ' videos.')
            print('**************Printing videos received**************')
            for video in videos:
                print(video)
                print('**********')
            input('Get more videos. Press enter')
            
