import pandas as pd
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from matplotlib.backends.backend_pdf import PdfPages

sns.set(style="whitegrid")

path = "/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/"

# Log file
log_file = path + "logfile.log"

def log_message(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}: {message}\n")

try:

  # Load your data (replace 'df' with your actual DataFrame)
    df = pd.read_csv('cleaned_data.csv')

    # Parse the input string
    input_string = "2024-05-16 01:07:28-04:00"
    parsed_datetime_iso = datetime.fromisoformat(input_string)

    # Convert 'Timestamp' column to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="mixed")

    # Convert the timezone of 'Timestamp' column to Eastern Standard Time (EST)
    df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')

    # Current subscriber count
    current_subscribers = df['MrBeast'].iloc[-1]

    # Calculate timestamp for 7 days ago and 1 day ago
    current_timestamp = datetime.now(pytz.timezone('Europe/Berlin'))

    # Convert the current timestamp to EST timezone
    current_timestamp = pd.to_datetime(current_timestamp).tz_convert('US/Eastern')

    start_timestamp_7_days = current_timestamp - timedelta(days=7)
    start_timestamp_1_day = current_timestamp - timedelta(days=1)

    # Filter rows for the last 7 days and 1 day
    df_last_7_days = df[df['Timestamp'] >= start_timestamp_7_days]
    df_last_1_day = df[df['Timestamp'] >= start_timestamp_1_day]

    # Current subscriber count
    current_subscribers = df['MrBeast'].iloc[-1]

    # Calculate hourly and minutely gains for the past 24 hours
    start_timestamp_24_hours = current_timestamp - timedelta(hours=24)
    previous_hour = current_timestamp - timedelta(hours=1)

    df_last_24_hours = df[(df['Timestamp'] >= start_timestamp_24_hours) & (df['Timestamp'] <= previous_hour)]

    # Initialize a list to store hourly gains for the past 24 hours
    hourly_gains_last_24_hours = []

    # Iterate over each hour within the past 24 hours
    for i in range(24):
        # Calculate the timestamp for the current hour
        current_hour = current_timestamp - timedelta(hours=i+1)
        start_hour = current_hour.replace(minute=0, second=0, microsecond=0)
        end_hour = current_hour.replace(minute=59, second=59, microsecond=999999)
        
        # Filter rows for the current hour
        df_current_hour = df[(df['Timestamp'] >= start_hour) & (df['Timestamp'] <= end_hour)]

        # Calculate hourly gains for the current hour
        if len(df_current_hour) > 1:
            hourly_gains = df_current_hour['MrBeast'].max() - df_current_hour['MrBeast'].min()
        else:
            hourly_gains = 0  # No data available for the current hour
            
        if i == 0:
            minutely_gains = round(hourly_gains / 60)
            secondly_gains = round(hourly_gains / 3600)

        # Append the hourly gains to the list
        hourly_gains_last_24_hours.append(hourly_gains)

    # Reverse the list to have the hourly gains in chronological order
    # hourly_gains_last_24_hours = hourly_gains_last_24_hours[::-1]


    # Subs gained today
    subs_gained_today = sum(hourly_gains_last_24_hours)

    # Subs gained in the last 7 days
    if len(df_last_7_days) > 1:
        subs_gained_last_7_days = df_last_7_days.iloc[-1]['MrBeast'] - df_last_7_days.iloc[0]['MrBeast']
    else:
        subs_gained_last_7_days = "Data not available"

    # Subs gained in the last 1 day
    if len(df_last_1_day) > 1:
        subs_gained_last_1_day = df_last_1_day.iloc[-1]['MrBeast'] - df_last_1_day.iloc[0]['MrBeast']
    else:
        subs_gained_last_1_day = "Data not available"

    # Subs gained since release
    subs_gained_since_release = current_subscribers - df['MrBeast'].iloc[0]

    # Calculate timestamp for the beginning of the day and the beginning of the week in EST timezone
    start_day = current_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    start_week = start_day - timedelta(days=start_day.weekday())

    # Filter rows for the last 7 days and the last 7 weeks
    df_last_7_days = df[(df['Timestamp'] >= start_day - timedelta(days=6)) & (df['Timestamp'] <= start_day)]
    df_last_7_weeks = df[(df['Timestamp'] >= start_week - timedelta(weeks=6)) & (df['Timestamp'] <= start_week)]

    # Calculate daily gains for the last 7 days
    daily_gains_last_7_days = df_last_7_days.groupby(df_last_7_days['Timestamp'].dt.date)['MrBeast'].last() - df_last_7_days.groupby(df_last_7_days['Timestamp'].dt.date)['MrBeast'].first()

    # Calculate weekly gains for the last 7 weeks
    weekly_gains_last_7_weeks = df_last_7_weeks.groupby(df_last_7_weeks['Timestamp'].dt.isocalendar().week)['MrBeast'].last() - df_last_7_weeks.groupby(df_last_7_weeks['Timestamp'].dt.isocalendar().week)['MrBeast'].first()

    # Group by date and hour, then sum to get total subscriber gains for each hour
    subscriber_gains_by_date_hour = df.groupby([df['Timestamp'].dt.date, df['Timestamp'].dt.hour])['MrBeast'].last() - df.groupby([df['Timestamp'].dt.date, df['Timestamp'].dt.hour])['MrBeast'].first()

    # Sort the hourly gains in descending order and select the top 15 hours
    top_15_hours_by_subscriber_gains = subscriber_gains_by_date_hour.sort_values(ascending=False).head(15)

    # Define the current timestamp
    current_timestamp = datetime.now(pytz.timezone('US/Eastern'))


    # Define styles
    styles = getSampleStyleSheet()
    bold_blue_style = ParagraphStyle(name='BoldBlue', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.blue)

    # Create a summary page
    with PdfPages(path + 'results.pdf') as pdf:
        # Create a summary page
        fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 size
        ax.axis('off')
        # Create the text with bold and color
        text = f"""
        Summary Report:

        Current Timestamp (EST): {current_timestamp}

        Current Subscribers: {current_subscribers}

        Minutely Gains: {minutely_gains}
        Secondly Gains: {secondly_gains}
        Subs Gained Today: {subs_gained_today}

        Subs Gained In The Last 7 Days: {subs_gained_last_7_days}
        Subs Gained In The Last 1 Day: {subs_gained_last_1_day}
        Subs Gained Since Release: {subs_gained_since_release}

        Hourly Gains (Last 24 Hours): {', '.join(map(str, hourly_gains_last_24_hours))}

        Daily Gains in The Last 7 Days:
        {', '.join(map(str, daily_gains_last_7_days))}

        Weekly Gains in The Last 7 Weeks:
        {', '.join(map(str, weekly_gains_last_7_weeks))}

        Top 15 hours by Subscriber Gains:
        {', '.join(map(str, top_15_hours_by_subscriber_gains))}
        """

        # Create the paragraph with bold and color
        #paragraph = Paragraph(text, bold_blue_style)

        ax.text(0.1, 0.5, text, fontsize=12, verticalalignment='center', transform=ax.transAxes, wrap=True)
        pdf.savefig(fig)
        plt.close()

        # Plot total subscriber gains over time
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        df['MrBeast'].plot(ax=ax, title='Total Subscriber Gains Over Time', color='b', linewidth=2)
        ax.set_xlabel('Time')
        ax.set_ylabel('Subscribers')
        ax.grid(True)
        pdf.savefig(fig)
        plt.close()

        # Plot hourly gains for the past 24 hours
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        sns.lineplot(x=range(24), y=hourly_gains_last_24_hours, ax=ax, marker='o', color='g')
        ax.set_title('Hourly Subscriber Gains (Last 24 Hours)')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Subscribers Gained')
        ax.grid(True)
        pdf.savefig(fig)
        plt.close()

        # Plot daily gains for the last 7 days
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        daily_gains_last_7_days.plot(ax=ax, kind='bar', title='Daily Subscriber Gains (Last 7 Days)', color='m')
        ax.set_xlabel('Date')
        ax.set_ylabel('Subscribers Gained')
        ax.grid(True)
        pdf.savefig(fig)
        plt.close()

        # Plot weekly gains for the last 7 weeks
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        weekly_gains_last_7_weeks.plot(ax=ax, kind='bar', title='Weekly Subscriber Gains (Last 7 Weeks)', color='c')
        ax.set_xlabel('Week')
        ax.set_ylabel('Subscribers Gained')
        ax.grid(True)
        pdf.savefig(fig)
        plt.close()

        # Plot top 15 hours by subscriber gains
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        top_15_hours_by_subscriber_gains.plot(ax=ax, kind='bar', title='Top 15 Hours by Subscriber Gains', color='r')
        ax.set_xlabel('Date and Hour')
        ax.set_ylabel('Subscribers Gained')
        ax.grid(True)
        pdf.savefig(fig)
        plt.close()

    log_message("Script executed successfully and results saved to PDF.")

except Exception as e:
    log_message(f"Error: {str(e)}")
    