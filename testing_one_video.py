import json
import requests
from pprint import pprint
from constants import API_KEY
from kafka import KafkaProducer

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers = ['localhost:9092'])
    response = requests.get("https://www.googleapis.com/youtube/v3/videos",
                            {
                                "key": API_KEY,
                                "id" : "gkPMpN9EUDM",
                                "part": "snippet,statistics,status"
                            })
    response = json.loads(response.text)['items']
    for video in response:
        print(video)
        video_response = {
            'title': video['snippet']['title'],
            'likes': int(video['statistics'].get('likeCount', 0)),
            'comments': int(video['statistics'].get('commentCount', 0)),
            'views': int(video['statistics'].get('viewCount', 0)),
            'favorites': int(video['statistics'].get('favoriteCount', 0)),
            'thumbnails': video['snippet']['thumbnails']['default']['url']
        }
        print(pprint(video_response))
        producer.send('youtube_videos', json.dumps(video_response).encode('utf-8'))
        producer.flush()