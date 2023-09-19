from rest_framework import viewsets
from .models import URLModel
from .serializers import URLModelSerializer
import re
from django_ratelimit.decorators import ratelimit
import openai
import random
import requests
import praw
import datetime
from rest_framework.decorators import api_view
import uuid
from googleapiclient.discovery import build
from django.http import StreamingHttpResponse
import openai
import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
import warnings
warnings.filterwarnings("ignore")
# <-------------------------------- LOADING MODEL CODE ------------------------------------------------->


# <-------------------------- GPT4 CODE FOR TEXT SUMMARIZATION AND KEYWORD EXTRACTION -------------------------->
session_data = {}  # e.g. {'some-session-id': {'comments': [], 'processed': False}}
@ratelimit(key='ip', rate='50/m')  # Allows 5 requests per minute per IP
@api_view(['POST'])
def store_comments(request):
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        data = json.loads(request.body.decode('utf-8'))
        comments = data.get('comments', [])
        session_id = str(uuid.uuid4())
        session_data[session_id] = {'comments': comments, 'processed': False}
        return JsonResponse({'sessionId': session_id})


@ratelimit(key='ip', rate='50/m')
def Summary(request, session_id):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return StreamingHttpResponse("Rate limit exceeded", content_type='text/event-stream', status=429)
    # Retrieve comments based on session_id
    session_info = session_data.get(session_id, {})
    comments = session_info.get('comments', [])

    if session_info.get('processed', False):
        return JsonResponse({'error': 'This session ID has already been processed.'})

    # Mark this session as processed
    session_data[session_id]['processed'] = True

    question = "Summarize these comments: " + ' '.join(comments)

    def event_stream():
        API_KEY = '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'
        openai.api_key = API_KEY
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": question}],
            temperature=0,
            stream=True
        )

        for chunk in response:
            chunk_str = json.dumps(chunk)
            data = json.loads(chunk_str)
            choices = data["choices"]

            for choice in choices:
                if "content" in choice["delta"]:
                    content = choice["delta"]["content"]
                    # print(content)
                    if "\n" in content:
                        content = content.replace("\n", "/n")
                    yield f"data: {content}\n\n"

        yield "event: done\ndata: \n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


@ratelimit(key='ip', rate='50/m')
def Keywords(request, session_id):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return StreamingHttpResponse("Rate limit exceeded", content_type='text/event-stream', status=429)
    # Retrieve comments based on session_id
    session_info = session_data.get(session_id, {})
    comments = session_info.get('comments', [])

    if session_info.get('processed', False):
        return JsonResponse({'error': 'This session ID has already been processed.'})

    # Mark this session as processed
    session_data[session_id]['processed'] = True
    question = "Top 5 Proper nouns: " + ' '.join(comments)

    def event_stream():
        API_KEY = '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'
        openai.api_key = API_KEY
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": question}],
            temperature=0,
            stream=True
        )

        for chunk in response:
            chunk_str = json.dumps(chunk)
            data = json.loads(chunk_str)
            choices = data["choices"]

            for choice in choices:
                if "content" in choice["delta"]:
                    content = choice["delta"]["content"]
                    # print(content)
                    if "\n" in content:
                        content = content.replace("\n", "/n")
                    yield f"data: {content}\n\n"

        yield "event: done\ndata: \n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


def extract_id(url):
    reddit_pattern = r'https://www\.reddit\.com/r/\w+/comments/([\w\d]+)/'
    youtube_pattern = r'https://www\.youtube\.com/watch\?v=([\w\d-]+)'
    youtube_shorts_pattern = r'https://www\.youtube\.com/shorts/([\w\d-]+)'

    reddit_match = re.search(reddit_pattern, url)
    youtube_match = re.search(youtube_pattern, url)
    youtube_shorts_match = re.search(youtube_shorts_pattern, url)

    if reddit_match:
        return fetch_reddit_comments(reddit_match.group(1))
    elif youtube_match:
        return fetch_youtube_info(youtube_match.group(1))
    elif youtube_shorts_match:
        return fetch_youtube_info(youtube_shorts_match.group(1))
    else:
        return 'Invalid URL'


def fetch_reddit_comments(post_id):
    
    Dictionary = {}
    try:
        reddit = praw.Reddit(
            client_id="lWclWhAZ4yBAnti784U79g",
            client_secret="dmvg0Jlhi-blpqo1GjJtO-1dpWURvQ",
            user_agent="CommentsAI (by u/RhubarbAgreeable1509)",
        )
        # Get the post and its comments
        submission = reddit.submission(id=post_id)
        # Convert UNIX timestamp to human-readable date
        date_posted = datetime.datetime.utcfromtimestamp(
            submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        print('Fetching Reddit data: ')
        # print("Title:", submission.title)
        # print("Posted by:", submission.author)
        # print("Date:", date_posted)
        # print("Subreddit:", submission.subreddit)
        # print('Media', submission.media)
        # print("Upvotes:", submission.ups)
        # print('Category', submission.category)
        # print("Downvotes:", submission.downs) 
        # print("Text:", submission.selftext) # Description
        # # can be used to show how popular the post is
        # print('Number of comments: ', submission.num_comments)
        # print('NSFW?: ', submission.over_18)  # If the post is NSFW or not
        # # Shows how likable the post is
        # print('Likability Index', submission.upvote_ratio)
        submission.comments.replace_more(limit=1)
        comments = submission.comments.list()
        # Build a DataFrame from the comments
        image_url = None
        if submission.url:
            image_extensions = ['jpg', 'jpeg', 'png', 'gif']
            if any(submission.url.lower().endswith(ext) for ext in image_extensions):
                image_url = submission.url
            else:
                image_url = ""

        video_url = None
        # Check if the submission has a media dictionary and if it has a 'reddit_video' key
        if submission.media and 'reddit_video' in submission.media:
            fallback_url = submission.media['reddit_video'].get('fallback_url', None)
            if fallback_url:
                video_url = fallback_url
            else:
                video_url = ""

        reddit_info = {
            'title' : submission.title,
            'published_at' : date_posted,
            'subreddit' : submission.subreddit.display_name,
            'downvotes' : submission.downs,
            'upvotes' : submission.ups,
            'num_comments' : submission.num_comments,
            'nsfw' : submission.over_18,
            'upvote_ratio' : submission.upvote_ratio,
            'description' : submission.selftext,
            'post_image' : image_url,
            'post_video' : video_url,
        }

        Dictionary['reddit_info'] = reddit_info

        subreddit_info = {
            'title' : submission.subreddit.title,
            'description' : submission.subreddit.description,
            'subscribers' : submission.subreddit.subscribers,
            'active_users' : submission.subreddit.active_user_count,
            'created_at' : datetime.datetime.utcfromtimestamp(submission.subreddit.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        }

        Dictionary['subreddit_info'] = subreddit_info

        data = {'Comments': []}
        meter = 0
        for comment in comments:
            if meter == 100:
                break
            data['Comments'].append(comment.body)
            meter += 1
        df = pd.DataFrame(data)
        df = df[df['Comments'] != '[removed]']
        # print(df)
        Dictionary['comments'] = json.loads(df.to_json(orient='records'))
        print(Dictionary)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    return Dictionary


def fetch_youtube_info(video_id):
    Dictionary = {}
    api_key = 'AIzaSyA4CEs3IPYXnGOn6eb6ayVDIFK7ZtnBq9s'
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
    except Exception as e:
        print(f"Could not build YouTube API client: {e}")
        return None

    try:
        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        data = response.json()
    except requests.Timeout:
        print("Request timed out.")
        return None
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding the response into JSON.")
        return None

    # More code to process 'data' ...
    if 'items' in data and len(data['items']) > 0:

        video_item = data['items'][0]['snippet']

        # published_at = video_item['publishedAt']
        # title = video_item['title']
        # description = video_item['description']
        # channel_title = video_item['channelTitle']
        # maxres_thumbnail_url = video_item['thumbnails']['high']['url']
        # tags = video_item['tags'][:10]
        channel_id = video_item['channelId']
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )

        response = request.execute()

        # The statistics of the video

        # print(f'Published At: {published_at}')
        # print(f'Title: {title}')
        # print(f'Description: {description}')
        # print(f'Channel Title: {channel_title}')
        # print(f'Max Res Thumbnail URL: {maxres_thumbnail_url}')
        # print(f'Tags: {", ".join(tags)}')

        video_info = {
            'published_at': video_item['publishedAt'],
            'title': video_item['title'],
            'description': video_item['description'],
            'channel_title': video_item['channelTitle'],
            'maxres_thumbnail_url': video_item['thumbnails']['high']['url'],
            'tags': video_item['tags'][:3] if 'tags' in video_item and len(video_item['tags']) > 0 else None,
            'statistics': response['items'][0]['statistics']
        }

        Dictionary['video_info'] = video_info
        if channel_id:
            channel_info = get_channel_info(channel_id, api_key)
            if channel_info:
                # print(json.dumps(channel_info, indent=4))
                a = channel_info['snippet']
                channel_info_selected = {
                    'channel_title': a['title'],
                    'channel_description': a['description'],
                    'channel_published_at': a['publishedAt'],
                    'channel_statistics': channel_info['statistics']
                }

                Dictionary['channel_info'] = channel_info_selected

            else:
                print("Could not fetch channel information.")
        else:
            print("Could not fetch channel ID.")

    else:
        print("Video not found or API request failed.")

    try:
        comments = []

        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100  # default is 20, max is 100
        ).execute()

        i = 1300
        while results and i < 1500:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # check if there are more comments
            if 'nextPageToken' in results:
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    pageToken=results['nextPageToken'],
                    textFormat='plainText',
                    maxResults=100
                ).execute()
                i += 100
            else:
                #         print(text)
                break

        print('The length of the comments', len(comments))
        # Create a DataFrame from the list of comments
        df = pd.DataFrame(comments, columns=['Comments'])
        # print(df)
        Dictionary['comments'] = json.loads(df.to_json(orient='records'))

    except Exception as e:
        print(f"An error occurred while fetching comments: {e}")
        return None

    return Dictionary

# <------------------------------- Getting Youtube Channel Information -------------------------------------->


def get_channel_info(channel_id, api_key):
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?id={channel_id}&key={api_key}&part=snippet,contentDetails,statistics"
    response = requests.get(channel_url)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]
    else:
        return None

@csrf_exempt
def fetch_sentiment(request):
    if request.method == 'POST':
        start = time.time()
        data = json.loads(request.body.decode('utf-8'))
        comments = data.get('comments')
        
        # Get the first 30 comments
        first_30_comments = comments[:15]

        # Exclude the first 30 comments
        remaining_comments = comments[15:]

        # Randomly select 30 comments from the remaining comments
        if len(remaining_comments) >= 15:
            random_30_comments = random.sample(remaining_comments, 15)
        else:
            random_30_comments = remaining_comments  # Take all if less than 15
        
        # Combine first 30 and random 30 comments
        selected_comments = first_30_comments + random_30_comments
        

        sentiment_api_url = "https://sentimentcloud-uikhbv3hna-uc.a.run.app/sentiment"

        try:
            sentiment_response = requests.post(sentiment_api_url, json=selected_comments)
            sentiment_response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return JsonResponse({"error": "Failed to get sentiment data"}, status=500)

        try:
            sentiment_response_data = json.loads(sentiment_response.text)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to decode sentiment data"}, status=500)
        
        end = time.time()
        print(sentiment_response_data, "Sentiment time", end - start)
        return JsonResponse({"sentiment": sentiment_response_data})

@csrf_exempt
def fetch_emotion(request):
    if request.method == 'POST':
        start = time.time()
        data = json.loads(request.body.decode('utf-8'))
        comments = data.get('comments')

        # Get the first 30 comments
        first_30_comments = comments[:15]

        # Exclude the first 30 comments
        remaining_comments = comments[15:]

        # Randomly select 30 comments from the remaining comments
        if len(remaining_comments) >= 15:
            random_30_comments = random.sample(remaining_comments, 15)
        else:
            random_30_comments = remaining_comments  # Take all if less than 30

        # Combine first 30 and random 30 comments
        selected_comments = first_30_comments + random_30_comments

        emotion_api_url = "https://emotioncloud-qvklogf5la-uc.a.run.app/emotion"

        try:
            emotion_response = requests.post(emotion_api_url, json=selected_comments)
            emotion_response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return JsonResponse({"error": "Failed to get emotion data"}, status=500)

        try:
            emotion_response_data = json.loads(emotion_response.text)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to decode emotion data"}, status=500)

        end = time.time()
        print(emotion_response_data, "Execution Time", end - start)
        return JsonResponse({"emotion": emotion_response_data})

@csrf_exempt
def fetch_cyber(request):
    if request.method == 'POST':
        start = time.time()
        data = json.loads(request.body.decode('utf-8'))
        comments = data.get('comments')

        # Get the first 30 comments
        first_30_comments = comments[:10]

        # Exclude the first 30 comments
        remaining_comments = comments[10:]

        # Randomly select 30 comments from the remaining comments
        if len(remaining_comments) >= 5:
            random_30_comments = random.sample(remaining_comments, 5)
        else:
            random_30_comments = remaining_comments  # Take all if less than 30

        # Combine first 30 and random 30 comments
        selected_comments = first_30_comments + random_30_comments

        cyber_api_url = "https://cybercloudmain-pizqny23ma-uc.a.run.app/cyber"

        try:
            cyber_response = requests.post(cyber_api_url, json=selected_comments)
            cyber_response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return JsonResponse({"error": "Failed to get emotion data"}, status=500)

        try:
            cyber_response_data = json.loads(cyber_response.text)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to decode emotion data"}, status=500)

        end = time.time()
        response = JsonResponse({"cyber": cyber_response_data})
        response["Access-Control-Allow-Origin"] = "*"
        return response


class URLModelViewSet(viewsets.ModelViewSet):
    queryset = URLModel.objects.all()
    serializer_class = URLModelSerializer

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        JsonDict = extract_id(url)  # Use your existing function

        # Check if JsonDict is a string and stop if it is
        if isinstance(JsonDict, str):
            # \033[91m is the ANSI escape code for red text
            print("\033[91mInvalid URL\033[0m")
            return JsonResponse({'error': 'Invalid data type for JsonDict'})

        # Additional validation to check if 'comments' key exists in JsonDict
        if 'comments' not in JsonDict:
            return JsonResponse({'error': 'No comments found in JsonDict'})
        

        return JsonResponse({'data': JsonDict})
