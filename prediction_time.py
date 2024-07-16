import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create the results directory if it doesn't exist
results_dir = '/Users/saadiaiftikhar/Documents/GitHub/vs_data/results/'
os.makedirs(results_dir, exist_ok=True)

# Load the CSV files
ucx_data = pd.read_csv('/Users/saadiaiftikhar/Documents/GitHub/vs_data/UCX6OQ3DkcsbYNE6H8uQQuVA.csv')
ucozwej_data = pd.read_csv('/Users/saadiaiftikhar/Documents/GitHub/vs_data/UCozwejESfvl88CBBL0KgEhw.csv')

# Convert the 'last_updated' column to datetime
ucx_data['last_updated'] = pd.to_datetime(ucx_data['last_updated'], utc=True)
ucozwej_data['last_updated'] = pd.to_datetime(ucozwej_data['last_updated'], utc=True)

# Check the range of dates before filtering
print("UCX Data Date Range Before Filtering:")
print(ucx_data['last_updated'].min(), ucx_data['last_updated'].max())
print("UCOZWEJ Data Date Range Before Filtering:")
print(ucozwej_data['last_updated'].min(), ucozwej_data['last_updated'].max())

# Print the number of rows before filtering
print(f"Number of rows in UCX data before filtering: {len(ucx_data)}")
print(f"Number of rows in UCOZWEJ data before filtering: {len(ucozwej_data)}")

# Filter the data to start from May 24th, 2023
start_date = pd.Timestamp('2023-05-27', tz='UTC')
ucx_data_filtered = ucx_data[ucx_data['last_updated'] >= start_date]
ucozwej_data_filtered = ucozwej_data[ucozwej_data['last_updated'] >= start_date]

# Find the latest starting point in both datasets
latest_start_date = max(ucx_data_filtered['last_updated'].min(), ucozwej_data_filtered['last_updated'].min())
ucx_data_filtered = ucx_data_filtered[ucx_data_filtered['last_updated'] >= latest_start_date]
ucozwej_data_filtered = ucozwej_data_filtered[ucozwej_data_filtered['last_updated'] >= latest_start_date]

# Print the number of rows after filtering
print(f"Number of rows in UCX data after filtering: {len(ucx_data_filtered)}")
print(f"Number of rows in UCOZWEJ data after filtering: {len(ucozwej_data_filtered)}")

# Check the range of dates after filtering
print("UCX Data Date Range After Filtering:")
print(ucx_data_filtered['last_updated'].min(), ucx_data_filtered['last_updated'].max())
print("UCOZWEJ Data Date Range After Filtering:")
print(ucozwej_data_filtered['last_updated'].min(), ucozwej_data_filtered['last_updated'].max())

# Normalize the previous_sub_count in ucx_data_filtered by subtracting 260,577,905
ucx_data_filtered['previous_sub_count'] = ucx_data_filtered['previous_sub_count'] - 260577905

# Sort the data by 'last_updated'
ucx_data_filtered = ucx_data_filtered.sort_values(by='last_updated')
ucozwej_data_filtered = ucozwej_data_filtered.sort_values(by='last_updated')

# Plot the historical data from May 27th, 2024
plt.figure(figsize=(14, 7))
plt.plot(ucx_data_filtered['last_updated'], ucx_data_filtered['previous_sub_count'], label='MB')
plt.plot(ucozwej_data_filtered['last_updated'], ucozwej_data_filtered['previous_sub_count'], label='HKO')
plt.xlabel('Date')
plt.ylabel('Subscriber Count')
plt.title('Historical Subscriber Counts from May 27th, 2024')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(results_dir, 'historical_subscriber_counts.png'))
plt.close()

# Forecasting future subscriber counts based on the average growth rate from the filtered data
ucx_latest_date = ucx_data_filtered['last_updated'].max()
ucx_previous_subs = ucx_data_filtered['previous_sub_count'].iloc[-2]
ucx_latest_subs = ucx_data_filtered['previous_sub_count'].iloc[-1]
ucx_avg_growth_per_day = ucx_data_filtered['average_per_day'].mean()

ucozwej_latest_date = ucozwej_data_filtered['last_updated'].max()
ucozwej_previous_subs = ucozwej_data_filtered['previous_sub_count'].iloc[-2]
ucozwej_latest_subs = ucozwej_data_filtered['previous_sub_count'].iloc[-1]
ucozwej_avg_growth_per_day = ucozwej_data_filtered['average_per_day'].mean()

# Generate future dates and predict subscriber counts minutely for the next day
forecast_range = pd.date_range(start=ucx_latest_date, periods=24, freq='T', tz='UTC')
#print(f'Forecast Range: {forecast_range}')
#print(ucozwej_data_filtered.head(3))

# `ucx_forecasted_subs` is a list that stores the forecasted subscriber counts for the next day for
# the 'MB' dataset (UCX data). Each element in the list represents the forecasted subscriber count at
# a specific minute within the next day. The forecast is based on the latest subscriber count, the
# average growth rate per day calculated from the filtered data, and the assumption that the growth
# rate remains constant over the next day.
ucx_forecasted_subs = [ucx_latest_subs + (ucx_latest_subs - ucx_avg_growth_per_day) * i for i in range(len(forecast_range))]
ucozwej_forecasted_subs = [ucozwej_latest_subs + (ucozwej_latest_subs - ucozwej_avg_growth_per_day) * i for i in range(len(forecast_range))]

print(f'UCX forecasted subscriber count for the next day: {ucx_forecasted_subs}')
print(f'UCOZWEJ forecasted subscriber count for the next day: {ucozwej_forecasted_subs}')

# Find the intersection point
intersection_date = None
for date, ucx_subs, ucozwej_subs in zip(forecast_range, ucx_forecasted_subs, ucozwej_forecasted_subs):
    if ucozwej_subs > ucx_subs:
        intersection_date = date
        break

# Plot the forecasted data for the next day
plt.figure(figsize=(14, 7))
plt.plot(forecast_range, ucx_forecasted_subs, label='MB (Forecast)')
plt.plot(forecast_range, ucozwej_forecasted_subs, label='HKO (Forecast)')
if intersection_date:
    plt.axvline(intersection_date, color='red', linestyle='--', label=f'Intersection: {intersection_date}')
plt.xlabel('Date')
plt.ylabel('Subscriber Count')
plt.title('Forecasted Subscriber Counts for the Next Day')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(results_dir, 'forecasted_subscriber_counts.png'))
plt.close()

print(f'Intersection date: {intersection_date}') if intersection_date else print('No intersection found.')

ucx_data_filtered.to_csv(results_dir + 'Filtered_UCX6OQ3DkcsbYNE6H8uQQuVA.csv', index=False)
ucozwej_data_filtered.to_csv(results_dir + 'Filtered_UCozwejESfvl88CBBL0KgEhw.csv', index=False)