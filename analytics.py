import json
import requests
import logging
from pprint import pprint
from constants import API_KEY, PLAYLIST_ID
from kafka import KafkaProducer

def fetch_page(url, parametars, page_token=None):
    """
    Function to fetch a page of data from the given URL with parameters.

    Args:
    - url: The URL to fetch data from.
    - parameters: Dictionary containing parameters to be sent with the request.
    - page_token: Token for paginated requests.

    Returns:
    - JSON response payload.
    """
    params = {**parametars, 'key': API_KEY, 'page_token': page_token}
    response = requests.get(url, params)
    payload = json.loads(response.text)
    logging.info("Response payload: %s", payload)

    return payload

def fetch_stream(url, parametars, page_token=None):
    """
    Function to fetch a stream of data from the given URL with parameters.

    Args:
    - url: The URL to fetch data from.
    - parameters: Dictionary containing parameters to be sent with the request.
    - page_token: Token for paginated requests.

    Yields:
    - Items from the fetched stream.
    """
    while True:
        payload = fetch_page(url, parametars, page_token)
        yield from payload['items']

        page_token = payload.get('nextPageToken')
        if page_token is None:
            break

def format_response(video):
    """
    Function to format the response JSON object containing video data.

    Args:
    - video: JSON object containing video data.

    Returns:
    - Formatted dictionary containing selected video attributes.
    """
    video_response = {
        'title': video['snippet']['title'],
        'likes': int(video['statistics'].get('likeCount', 0)),
        'comments': int(video['statistics'].get('commentCount', 0)),
        'views': int(video['statistics'].get('viewCount', 0)),
        'favorites': int(video['statistics'].get('favoriteCount', 0)),
        'thumbnails': video['snippet']['thumbnails']['default']['url']
    }
    return video_response


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    for video_item in fetch_stream(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            {"playlistId": PLAYLIST_ID, "part": "snippet,contentDetails"},
            None):
        video_id = video_item['contentDetails']['videoId']

        for video in fetch_stream(
                "https://www.googleapis.com/youtube/v3/videos",
                {'id': video_id, 'part': 'snippet,statistics'},
                None):
            # Uncomment the line below if you want to log the video information
            # logging.info("Video ID: %s", pprint(format_response(video)))
            producer.send('youtube_videos', json.dumps(format_response(video)).encode('utf-8'),
                          key=video_id.encode('utf-8'))
            print('Sent ', video['snippet']['title'])