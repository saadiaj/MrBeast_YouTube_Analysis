from googleapiclient.discovery import build
import csv
import isodate

# Replace with your API key
api_key = 'AIzaSyDpHj2ikrjl_HHzbSrTYWP9jdPU7lguneM'

# YouTube API client setup
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get video details
def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        video_data = response['items'][0]
        title = video_data['snippet']['title']
        views = video_data['statistics'].get('viewCount', 'N/A')
        likes = video_data['statistics'].get('likeCount', 'N/A')
        comments = video_data['statistics'].get('commentCount', 'N/A')
        duration = video_data['contentDetails']['duration']
        
        # Parse the duration to check if the video is a short
        duration_seconds = isodate.parse_duration(duration).total_seconds()
        is_short = duration_seconds < 60
        
        return {
            'title': title,
            'views': views,
            'likes': likes,
            'comments': comments,
            'is_short': is_short
        }
    else:
        return None

# Function to get video IDs from a channel
def get_video_ids(channel_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type="video"
        )
        response = request.execute()

        for item in response.get('items', []):
            video_ids.append(item['id']['videoId'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids

# Function to get all video details from a channel
def get_all_videos_details(channel_id):
    video_ids = get_video_ids(channel_id)
    videos_details = []

    for video_id in video_ids:
        details = get_video_details(video_id)
        if details:
            videos_details.append(details)
        print(f"Fetched details for video {video_id}")

    return videos_details

# Define your channel ID here
channel_id = 'UCX6OQ3DkcsbYNE6H8uQQuVA'  # Replace with the actual channel ID

# Fetch all videos details
videos_data = get_all_videos_details(channel_id)

# Print and/or save the data
for video in videos_data:
    print(f"Title: {video['title']}, Views: {video['views']}, Likes: {video['likes']}, Comments: {video['comments']}, Is Short: {video['is_short']}")

# Optionally, save to CSV
output_file = 'MB_channel_videos.csv'

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Views', 'Likes', 'Comments', 'Is Short'])
    
    for video in videos_data:
        writer.writerow([video['title'], video['views'], video['likes'], video['comments'], video['is_short']])

print(f"Data saved to {output_file}")
