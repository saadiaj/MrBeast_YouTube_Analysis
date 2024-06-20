import asyncio
import csv
import schedule
#import time
from datetime import datetime
from pytz import timezone
from pyppeteer import launch

async def fetch_subscriber_counts(page):
    try:
        # Navigate to the URL
        await page.goto("https://www.viewstats.com/mrbeastvstseries")

        # Wait for the subscriber count element to appear
        await page.waitForSelector('.index-module_slot_wrap__ZT-DX', {'timeout': 60000})

        # Evaluate a script in the context of the page to extract subscriber counts
        subscriber_counts = await page.evaluate('''() => {
            const elements = document.querySelectorAll('.index-module_slot_wrap__ZT-DX');
            return Array.from(elements).map(el => el.innerText);
        }''')
        #print("Subscriber counts:", subscriber_counts)

        # Function to clean and filter subscriber counts
        def clean_subscriber_counts(raw_counts):
            cleaned_counts = []
            for count in raw_counts:
                # Remove newlines and commas
                cleaned_number = count.replace('\n', '').replace(',', '')
                # Extract only the first occurrence of each digit pair
                unique_number = ''.join([cleaned_number[i] for i in range(0, len(cleaned_number), 2)])
                cleaned_counts.append(unique_number)
            return cleaned_counts

        # Clean the extracted subscriber counts
        cleaned_subscriber_counts = clean_subscriber_counts(subscriber_counts)

        middle_value = cleaned_subscriber_counts[1]
        
        # Save the cleaned data to a CSV file with EST timestamp
        est = timezone('US/Eastern')
        # Get the current timestamp in EST format
        timestamp = datetime.now(est).strftime('%Y-%m-%d %H:%M:%S.%f%z')  # Includes microseconds and timezone offset

        with open('cleaned_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Add a header row if the file is empty
            if file.tell() == 0:
                writer.writerow(['Timestamp', 'MrBeast'])
            writer.writerow([timestamp, str(middle_value)])
            
    except Exception as e:
        print("Error:", e)

async def main():
    # Launch the browser in headless mode
    browser = await launch(ignoreHTTPSErrors=True, headless=False)
    page = await browser.newPage()

    async def job():
        await fetch_subscriber_counts(page)

    # Schedule the task to run every minute
    schedule.every(1).minute.do(lambda: asyncio.ensure_future(job()))

    try:
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Close the browser
        await browser.close()

# Run the main function
asyncio.get_event_loop().run_until_complete(main())
