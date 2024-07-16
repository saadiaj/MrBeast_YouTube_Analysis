import csv
from googleapiclient.discovery import build
from datetime import datetime
import matplotlib.pyplot as plt

# Define the scopes for accessing YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# YouTube channel IDs
MB_channels = [
    ("UCX6OQ3DkcsbYNE6H8uQQuVA", "MrBeast"),
    ("UCluBATXIP9doWvougjUVUGQ", "MrBeast На Русском"),
    ("UCDifkiOICEJ-hiVAvCQlpNA", "MrBeast हिन्दी"),
    ("UCbHU7ouxaMgfyWSUtI4QK8Q", "MrBeast in Arabic"),
    ("UCNAhW2oJvy_FUU082pEDspA", "MrBeast en Español"),
    ("UCggERuskO1F6XKwor-Pvkww", "MrBeast Brasil"),
    ("UCbf2Ozi4BF34AY3t3rHj9IA", "MrBeast en Français"),
    ("UClwITvsAr6JnpLmGufudiTw", "MrBeast Japan"),
    ("UCUaT_39o1x6qWjz7K2pWcgw", "Beast Reacts"),
    ("UCneluyh2H6gU7v8gU8El-Cg", "Beast Reacts em Português"),
    ("UCLAVIBJWb6geGRSvWsZ_ang", "Beast Reacts На Русском"),
    ("UCL6Xc5xuRECnWbGBOKG9APA", "Beast Reacts en Español"),
    ("UCIPPMRA040LQr5QPyJEbmXA", "MrBeast Gaming"),
    ("UC1lZ05QnM1R09HiwNMLDdnw", "MrBeast Gaming На Русском"),
    ("UCfNGT03h99S3zLbyUD9FMuQ", "MrBeast Gaming en Español"),
    ("UCpPJaHR_s3qYSCzry78G7lg", "MrBeast Gaming Brasil"),
    ("UC4-79UOlP48-QNGgCko5p2g", "MrBeast 2"),
    ("UCAiLfjNXkNv24uhpzUgPa6A", "Beast Philanthropy"),
    ("UCZzvDDvaYti8Dd8bLEiSoyQ", "MrBeast 3"),
    ("UC68DIXWCmetC8N5J_Kc5gjQ", "Don't Subscribe")
]

# Function to authenticate and fetch subscriber count
def get_subscriber_count(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()

    if response['items']:
        subscriber_count = int(response['items'][0]['statistics']['subscriberCount'])
        return subscriber_count

    return None

# Function to fetch videos of a channel
def get_channel_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []

    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()

    while request:
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                # Filter videos published after 2020-01-01
                published_at = item['snippet']['publishedAt']
                if datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ') > datetime(2012, 1, 1):
                    videos.append(item['id']['videoId'])

        request = youtube.search().list_next(request, response)
        if request:
            response = request.execute()

    return videos

# Function to fetch video details
def get_video_details(api_key, video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_details = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="statistics,snippet",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for item in response['items']:
            # Check if the video is a short
            duration = item['snippet']['thumbnails'].get('standard') is None  # If standard thumbnail is not available, it's likely a short

            video_details.append({
                'id': item['id'],
                'title': item['snippet']['title'],
                'publishedAt': item['snippet']['publishedAt'],
                'viewCount': int(item['statistics'].get('viewCount', 0)),
                'likeCount': int(item['statistics'].get('likeCount', 0)),
                'commentCount': int(item['statistics'].get('commentCount', 0)),
                'isShort': duration
            })

    return video_details

# Function to write data to CSV
def write_to_csv(filename, data, video_data, totals):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel ID', 'Channel Name', 'Subscribers Count', 'Total Videos', 'Total Likes', 'Total Comments'])

        for channel_id, channel_data in data.items():
            writer.writerow([
                channel_id,
                channel_data['name'],
                channel_data['subscribers'],
                channel_data['total_videos'],
                channel_data['total_likes'],
                channel_data['total_comments']
            ])
        
        # Writing totals
        writer.writerow(['Total', '', totals['total_subscribers'], totals['total_videos'], totals['total_likes'], totals['total_comments']])

# Function to write video details to CSV
def write_video_details_to_csv(filename, video_data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Name', 'Video Title', 'Video ID', 'Published At', 'Likes', 'Comments', 'Is Short'])
        for video in video_data:
            writer.writerow([
                video['channelName'],
                video['title'],
                video['id'],
                video['publishedAt'],
                video['likeCount'],
                video['commentCount'],
                video['isShort']
            ])

# Function to plot graphs and save as image files
def plot_graphs(video_data):
    # Extract data for plotting
    views = [video['viewCount'] for video in video_data]
    likes = [video['likeCount'] for video in video_data]
    comments = [video['commentCount'] for video in video_data]
    is_short = [video['isShort'] for video in video_data]
    titles = [video['title'] for video in video_data]

    # Colors for short and non-short videos
    colors = ['red' if short else 'blue' for short in is_short]

    # Plot Likes vs Views
    plt.figure(figsize=(12, 6))
    plt.scatter(views, likes, c=colors, label='Videos')
    top10_likes_indices = sorted(range(len(likes)), key=lambda i: likes[i], reverse=True)[:10]
    for i in top10_likes_indices:
        plt.scatter(views[i], likes[i], c='yellow')
        plt.text(views[i], likes[i], titles[i], fontsize=9)
    plt.title('Likes vs Views')
    plt.xlabel('Views')
    plt.ylabel('Likes')
    plt.legend()
    plt.savefig('/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/likes_vs_views.png')
    plt.show()

    # Plot Comments vs Views
    plt.figure(figsize=(12, 6))
    plt.scatter(views, comments, c=colors, label='Videos')
    top10_comments_indices = sorted(range(len(comments)), key=lambda i: comments[i], reverse=True)[:10]
    for i in top10_comments_indices:
        plt.scatter(views[i], comments[i], c='yellow')
        plt.text(views[i], comments[i], titles[i], fontsize=9)
    plt.title('Comments vs Views')
    plt.xlabel('Views')
    plt.ylabel('Comments')
    plt.legend()
    plt.savefig('/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/comments_vs_views.png')
    plt.show()

    # Plot Top 10 Views
    plt.figure(figsize=(12, 6))
    plt.scatter(views, likes, c=colors, label='Videos')
    top10_views_indices = sorted(range(len(views)), key=lambda i: views[i], reverse=True)[:10]
    for i in top10_views_indices:
        plt.scatter(views[i], likes[i], c='yellow')
        plt.text(views[i], likes[i], titles[i], fontsize=9)
    plt.title('Top 10 Views vs Likes')
    plt.xlabel('Views')
    plt.ylabel('Likes')
    plt.legend()
    plt.savefig('/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/top10_views.png')
    plt.show()

# Main function
def main():
    # Your API key for YouTube Data API (replace with your own API key)
    api_key = 'AIzaSyBXqEsEk9s-4nyAl2nfwQyadxHBtQx8g_w'
    # 'AIzaSyDpHj2ikrjl_HHzbSrTYWP9jdPU7lguneM'

    # Dictionary to store all data
    all_data = {}
    all_video_data = []

    # Variables to store totals
    total_subscribers = 0
    total_videos = 0
    total_likes = 0
    total_comments = 0

    for channel_id, channel_name in MB_channels:
        print(f"Processing channel: {channel_name}")

        # Get subscriber count
        subscriber_count = get_subscriber_count(api_key, channel_id)
        if subscriber_count:
            total_subscribers += subscriber_count

        # Get channel videos
        video_ids = get_channel_videos(api_key, channel_id)

        # Get video details
        video_details = get_video_details(api_key, video_ids)

        # Aggregate data
        num_videos = len(video_ids)
        total_likes_channel = sum(video['likeCount'] for video in video_details)
        total_comments_channel = sum(video['commentCount'] for video in video_details)

        total_videos += num_videos
        total_likes += total_likes_channel
        total_comments += total_comments_channel

        all_data[channel_id] = {
            'name': channel_name,
            'subscribers': subscriber_count,
            'total_videos': num_videos,
            'total_likes': total_likes_channel,
            'total_comments': total_comments_channel
        }

        # Append video details with channel name
        for video in video_details:
            video['channelName'] = channel_name
            all_video_data.append(video)

    # Totals dictionary
    totals = {
        'total_subscribers': total_subscribers,
        'total_videos': total_videos,
        'total_likes': total_likes,
        'total_comments': total_comments
    }

    # Write summary data to CSV
    summary_output_file = '/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/MB_youtube_channels_totals.csv'
    write_to_csv(summary_output_file, all_data, all_video_data, totals)

    # Write video details to CSV
    details_output_file = '/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/MB_youtube_channels_details.csv'
    write_video_details_to_csv(details_output_file, all_video_data)

    # Plot graphs and save as images
    plot_graphs(all_video_data)

    print("Data written to", summary_output_file, "and", details_output_file)

if __name__ == "__main__":
    main()