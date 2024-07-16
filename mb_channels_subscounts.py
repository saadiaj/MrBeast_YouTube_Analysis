import csv
from googleapiclient.discovery import build

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

#"UCozwejESfvl88CBBL0KgEhw"

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

# Function to write data to CSV
def write_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel ID', 'Channel Name', 'Subscribers Count'])

        for channel_id, channel_name in MB_channels:
            subscribers_count = data.get(channel_id)
            writer.writerow([channel_id, channel_name, subscribers_count])

# Main function
def main():
    # Your API key for YouTube Data API (replace with your own API key)
    api_key = 'AIzaSyDpHj2ikrjl_HHzbSrTYWP9jdPU7lguneM'

    # Dictionary to store subscriber counts
    subscriber_counts = {}
    total_count = 0

    for channel_id, _ in MB_channels:
        count = get_subscriber_count(api_key, channel_id)
        if count:
            total_count += count
        subscriber_counts[channel_id] = count

    print(f'Total Subscribers of All MB channels are: {total_count + 933000}')
    
    # Write data to CSV
    output_file = '/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/MB_youtube_channels.csv'
    write_to_csv(output_file, subscriber_counts)

    print("Data written to", output_file)

if __name__ == "__main__":
    main()
