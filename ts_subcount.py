import csv
from googleapiclient.discovery import build

# Define the scopes for accessing YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Updated list of YouTube channel IDs
channels = [
    ('T-Series Bhakti Sagar', 'UCaayLD9i5x4MmIoVZxXSv_g'),
    ('T-Series Apna Punjab', 'UCcvNYxWXR_5TjVK7cSCdW-g'),
    ('T-Series StageWorks Academy', 'UCRm96I5kmb_iGFofE5N691w'),
    ('Pop Chartbusters', 'UCzL6rJhkoXkIt0fCv9T9_uA'),
    ('T-Series Regional', 'UCy2fvV-mH_4AcIgqnLg9uDw'),
    ('T-Series Hamaar Bhojpuri', 'UCpN-WGQgGsOrXm7nHXDdTDA'),
    ('T-Series Telugu', 'UCnJjcn5FrgrOEp5_N45ZLEQ'),
    ('T-Series Islamic Music', 'UCVkXfARLNI0vf7gajoDDjlw'),
    ('Shabad Gurbani', 'UC884UDwNldmpdEiS1mgtijA'),
    ('T-Series Kids Hut', 'UChz5aEi3dfrDVC8-YJsMUDA'),
    ('T-Series Movies', 'UCAEv0ANkT221wXsTnxFnBsQ'),
    ('T-Series Marathi', 'UCuphZ5BwKpxwqGDJBe6VRyg'),
    ('T-Series Kannada', 'UCovxnbWKPCA5iJDxa9zbBew'),
    ('T-Series Bhakti Marathi', 'UCR4_gSSeup7YpBfsOWN_oRA'),
    ('T-Series Gujarati', 'UCev6abkwjdHj_dB3rquFfbQ'),
    ('T-Series Haryanvi', 'UC3Zva7aW8lJUFZQYnC-XyHg'),
    ('T-Series Classical', 'UCCo_LMj-m3iGSSuytYq9n6Q'),
    ('T-Series Kids Hut ESP', 'UCBlslL5pqbe8EwI1Edx__Fw'),
    ('T-Series Malayalam', 'UCUoj77TIUy9DhLNe5EVmF-A'),
    ('T-Series Classical', 'UCH_dFsLe_I0ftAFP8XzJkTQ'),
    ('T-Series Kids Hut - Por. Fairy Tales', 'UCz2pmzVJkW78zzUNIN0GeTQ'),
    ('Bhakti Sagar Kannada', 'UCQX4SV8Fg0cD98K1VRBVPEw'),
    ('T-Series Bhavageethegalu & Folk', 'UCJKd5H8WR_w0wN-Or1-MJyQ'),
    ('Bhakti Sagar Telugu', 'UCjA7qIB2IetzeolMd_Hwa0w'),
    ('T-Series Tamil', 'UCoi3aLlLa6xs0A1QwR_7oxA'),
    ('T-Series Bhakti Sagar', 'UCvX5_TDQ3kJq48FF9xCvJ6Q'),
    ('Bhakti Sagar Tamil', 'UCg5bqGqi_ROdCPV4eHF575g'),
    ('Bhakti Sagar Malayalam', 'UCG-dSI2eRCBzxzPUfXjxHQw'),
    ('T-Series Himachali', 'UC6rzGFfqiyOTxIGhx7MDJYA'),
    ('T-Series Rajasthani', 'UCkPipkv-8UZ2saO2TjE8AWA'),
    ('T-Series Kashmiri Music', 'UCPH9W_9ZDQ1gemcCaIxOvCw'),
    ('T-Series Movies', 'UC_FsO0WQ3Haw3EQpPH_h0Bw'),
    ('T-Series', 'UCq-Fj5jknLsUf-MWSy4_brA'),
    ('Lahari Music', 'UCnSqxrSfo1sK4WZ7nBpYW1Q'),
    ('Lahari Music Telugu', 'UCyhgNoFwssv3hG-gc29sEnw'),
    ('Lahari Bhavageethegalu & Folk', 'UCXNtS5Od_4Njr6J5YJo2uyg'),
    ('Lahari Music Kannada', 'UC3nd8KWMTo8w_KOyPBs1HsA'),
    ('Lahari Music Tamil', 'UCN5cwheKFtBXLQCss18UgpA'),
    ('Bhakti Lahari Kannada', 'UCOb2IJpMET6r45eM-vzALiQ'),
    ('Lahari Music Malayalam', 'UCBi7UD8gdi_SCLX7dZjKVeQ'),
    ('Lahari Janapada Geethegalu', 'UCGi7QIJEPTi09j37z7kY2qg'),
    ('Lahari Karaoke I T-Series', 'UCZ8_6qvdkJQEhyXQEkEtQAQ'),
    ('Bhakti Lahari Tamil', 'UCDVDaxrGbc0g4QGgOh1lcqQ'),
    ('Bhakti Lahari Telugu', 'UC9VpXeB0L74sOIMTg-PQT-A'),
    ('Lahari Comedy T-Series', 'UCJySEUaIQjMA3uvCXh12qRA'),
    ('Lahari Classical', 'UCsQMWfiNhYtxVss-Z1Z2Aww'),
    ('T-Series Movies', 'UC2B3PVpLkCApYx1BMghmNnQ'),
    ('Bhakti Lahari Sanskrit', 'UC91yw44h6LhazKipp_ToWUw')
]

# Function to authenticate and fetch subscriber count
def get_subscriber_count(api_key, channel_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.channels().list(part="statistics", id=channel_id)
        response = request.execute()

        if response['items']:
            subscriber_count = int(response['items'][0]['statistics']['subscriberCount'])
            return subscriber_count
    except Exception as e:
        print(f"An error occurred for channel ID {channel_id}: {e}")

    return None

# Function to write data to CSV
def write_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Name', 'Channel ID', 'Subscribers Count'])

        for channel_name, channel_id in channels:
            subscribers_count = data.get(channel_id, 'N/A')
            writer.writerow([channel_name, channel_id, subscribers_count])

# Main function
def main():
    # Your API key for YouTube Data API (replace with your own API key)
    api_key = 'AIzaSyDpHj2ikrjl_HHzbSrTYWP9jdPU7lguneM'

    # Dictionary to store subscriber counts
    subscriber_counts = {}
    total_count = 0

    for channel_name, channel_id in channels:
        count = get_subscriber_count(api_key, channel_id)
        if count is not None:
            total_count += count
        subscriber_counts[channel_id] = count

    print(f'Total Subscribers of All TS channels are: {total_count + 798000}')
    
    # Write data to CSV
    output_file = '/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/TS_youtube_channels.csv'
    write_to_csv(output_file, subscriber_counts)

    print("Data written to", output_file)

if __name__ == "__main__":
    main()
