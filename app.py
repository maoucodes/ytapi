from youtubesearchpython import VideosSearch, Video, ResultMode
from flask import Flask, jsonify
import requests
from cachetools import cached, TTLCache

app = Flask(__name__)

# Configure cache with a Time-To-Live (TTL) of 1 hour and max size of 100 items
cache = TTLCache(maxsize=100, ttl=3600)

def fetch_video_info(video_id):
    response = requests.get(f'https://www.youtube.com/watch?v={video_id}')
    return response.json()

@app.route('/app/id/<video_id>')
def infoPage(video_id):
    if video_id in cache:
        return jsonify(cache[video_id])
    
    try:
        data = fetch_video_info(video_id)
        cache[video_id] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

def fetch_search_results(query):
    videosSearch = VideosSearch(query, limit=10)
    return videosSearch.result()

@app.route('/app/search/<query>')
def searchPage(query):
    if query in cache:
        return jsonify(cache[query])
    
    try:
        data = fetch_search_results(query)
        cache[query] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})