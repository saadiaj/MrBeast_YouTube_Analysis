import pandas as pd
from pytz import timezone
from datetime import datetime

# Read data from MrBeast_Subscribers_5.csv and rename columns
mrbeast_df = pd.read_csv('MrBeast_Subscribers.csv')
mrbeast_df.rename(columns={'Time (UTC)': 'Timestamp', 'Subscriber Count': 'MrBeast'}, inplace=True)

# Convert 'Timestamp' column in mrbeast_df to datetime with UTC timezone and then to EST
mrbeast_df['Timestamp'] = pd.to_datetime(mrbeast_df['Timestamp'], utc=True).dt.tz_convert('US/Eastern')

# Save the cleaned dataframe to a new CSV file
mrbeast_df.to_csv('cleaned_data.csv', index=False)
