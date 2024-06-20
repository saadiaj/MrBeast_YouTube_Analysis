import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import LabelEncoder

# Create a directory to save plots
plot_dir = 'plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Load the CSV file
file_path = 'MB_channel_videos.csv'
data = pd.read_csv(file_path)

# Display initial data types
print("Initial data types:\n", data.dtypes)

# Ensure numeric columns are properly converted to numeric types
numeric_columns = ['Views', 'Likes', 'Comments']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Check for non-numeric entries and print them
for col in numeric_columns:
    non_numeric_entries = data[pd.to_numeric(data[col], errors='coerce').isna()]
    if not non_numeric_entries.empty:
        print(f"Non-numeric entries found in column (col):\n", non_numeric_entries[[col, 'Title']])

# Replace NaNs with zeros
data.fillna(0, inplace=True)

# Calculate additional metrics: views/likes ratio and views/comments ratio
data['v_like_ratio'] = data['Views'] / data['Likes']
data['v_com_ratio'] = data['Views'] / data['Comments']

# Describe the data to get a summary of statistics
data_description = data.describe()

# Set up the plotting style
sns.set(style='whitegrid')

# 2. Relationship between Views and Likes with v_like_ratio
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Views', y='Likes', data=data, hue='Is Short', palette='coolwarm')
plt.title('Relationship between Views and Likes', fontsize=20)
plt.xlabel('Views', fontsize=18)
plt.ylabel('Likes', fontsize=18)

# Annotate outliers
threshold_x = data['Views'].quantile(0.99)
threshold_y = data['Likes'].quantile(0.99)
outliers = data[(data['Views'] > threshold_x) | (data['Likes'] > threshold_y)]
for i in range(outliers.shape[0]):
    plt.text(outliers['Views'].iloc[i], outliers['Likes'].iloc[i], outliers['Title'].iloc[i], fontsize=9)

plt.legend(title='Is Short')
plt.savefig(os.path.join(plot_dir, 'views_vs_likes.jpeg'))
plt.close()

# 3. Relationship between Views and Comments with v_com_ratio
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Views', y='Comments', data=data, hue='Is Short', palette='viridis')
plt.title('Relationship between Views and Comments', fontsize=20)
plt.xlabel('Views', fontsize=18)
plt.ylabel('Comments', fontsize=18)

# Annotate outliers
threshold_x = data['Views'].quantile(0.99)
threshold_y = data['Comments'].quantile(0.99)
outliers = data[(data['Views'] > threshold_x) | (data['Comments'] > threshold_y)]
for i in range(outliers.shape[0]):
    plt.text(outliers['Views'].iloc[i], outliers['Comments'].iloc[i], outliers['Title'].iloc[i], fontsize=9)

plt.legend(title='Is Short')
plt.savefig(os.path.join(plot_dir, 'views_vs_comments.jpeg'))
plt.close()

# Encode the categorical 'Is Short' data
le = LabelEncoder()
data['Is Short'] = le.fit_transform(data['Is Short'])

# 4. 3D plot for Views, Likes, and Comments with cmap='cool'
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(data['Views'], data['Likes'], data['Comments'], c=data['Is Short'], cmap='cool', s=50)
ax.set_xlabel('Views', fontsize=18)
ax.set_ylabel('Likes', fontsize=18)
ax.set_zlabel('Comments', fontsize=16)
plt.title('3D Plot of Views, Likes, and Comments', fontsize=20)
legend1 = ax.legend(*sc.legend_elements(), title="Is Short")
ax.add_artist(legend1)

# Annotate outliers
threshold_views = data['Views'].quantile(0.99)
threshold_likes = data['Likes'].quantile(0.99)
threshold_comments = data['Comments'].quantile(0.99)
outliers = data[(data['Views'] > threshold_views) | (data['Likes'] > threshold_likes) | (data['Comments'] > threshold_comments)]

for i in range(outliers.shape[0]):
    ax.text(outliers['Views'].iloc[i], outliers['Likes'].iloc[i], outliers['Comments'].iloc[i], 
            outliers['Title'].iloc[i], fontsize=9, color='black', weight='bold', style='italic')

# Highlight outliers with larger points
ax.scatter(outliers['Views'], outliers['Likes'], outliers['Comments'], c='red', s=100, edgecolor='k', label='Outliers')

plt.savefig(os.path.join(plot_dir, '3d_plot_views_likes_comments_cool.jpeg'))
plt.close()




# # 1. Distribution of Views, Likes, Comments, v_like_ratio, and v_com_ratio
# plt.figure(figsize=(18, 10))

# plt.subplot(2, 3, 1)
# sns.histplot(data['Views'], bins=30, kde=True, color='blue')
# plt.title('Distribution of Views')

# plt.subplot(2, 3, 2)
# sns.histplot(data['Likes'], bins=30, kde=True, color='green')
# plt.title('Distribution of Likes')

# plt.subplot(2, 3, 3)
# sns.histplot(data['Comments'], bins=30, kde=True, color='red')
# plt.title('Distribution of Comments')

# plt.subplot(2, 3, 4)
# sns.histplot(data['v_like_ratio'].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, kde=True, color='purple')
# plt.title('Distribution of Views/Likes Ratio')

# plt.subplot(2, 3, 5)
# sns.histplot(data['v_com_ratio'].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, kde=True, color='orange')
# plt.title('Distribution of Views/Comments Ratio')

# plt.tight_layout()
# plt.savefig(os.path.join(plot_dir, 'distribution_views_likes_comments_ratios.jpeg'))
# plt.close()


# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# import os
# from mpl_toolkits.mplot3d import Axes3D
# from sklearn.preprocessing import LabelEncoder

# # Create a directory to save plots
# plot_dir = 'plots'
# if not os.path.exists(plot_dir):
#     os.makedirs(plot_dir)

# # Load the CSV file
# file_path = 'MB_channel_videos.csv'
# data = pd.read_csv(file_path)

# # Display initial data types
# print("Initial data types:\n", data.dtypes)

# # Ensure numeric columns are properly converted to numeric types
# numeric_columns = ['Views', 'Likes', 'Comments']
# for col in numeric_columns:
#     data[col] = pd.to_numeric(data[col], errors='coerce')

# # Check for non-numeric entries and print them
# for col in numeric_columns:
#     non_numeric_entries = data[pd.to_numeric(data[col], errors='coerce').isna()]
#     if not non_numeric_entries.empty:
#         print(f"Non-numeric entries found in column (col}:\n", non_numeric_entries[[col, 'Title']])

# # Replace NaNs with zeros
# data.fillna(0, inplace=True)

# # Calculate additional metrics: views/likes ratio and views/comments ratio
# data['v_like_ratio'] = data['Views'] / data['Likes']
# data['v_com_ratio'] = data['Views'] / data['Comments']

# # Describe the data to get a summary of statistics
# data_description = data.describe()

# # Set up the plotting style
# sns.set(style='whitegrid')

# # 1. Distribution of Views, Likes, Comments, v_like_ratio, and v_com_ratio
# plt.figure(figsize=(18, 10))

# plt.subplot(2, 3, 1)
# sns.histplot(data['Views'], bins=30, kde=True, color='blue')
# plt.title('Distribution of Views')

# plt.subplot(2, 3, 2)
# sns.histplot(data['Likes'], bins=30, kde=True, color='green')
# plt.title('Distribution of Likes')

# plt.subplot(2, 3, 3)
# sns.histplot(data['Comments'], bins=30, kde=True, color='red')
# plt.title('Distribution of Comments')

# plt.subplot(2, 3, 4)
# sns.histplot(data['v_like_ratio'].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, kde=True, color='purple')
# plt.title('Distribution of Views/Likes Ratio')

# plt.subplot(2, 3, 5)
# sns.histplot(data['v_com_ratio'].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, kde=True, color='orange')
# plt.title('Distribution of Views/Comments Ratio')

# plt.tight_layout()
# plt.savefig(os.path.join(plot_dir, 'distribution_views_likes_comments_ratios.jpeg'))
# plt.close()

# # 2. Relationship between Views and Likes with v_like_ratio
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='Views', y='Likes', data=data, hue='Is Short', palette='coolwarm')
# plt.title('Views vs Likes')
# plt.xlabel('Views')
# plt.ylabel('Likes')

# # Annotate outliers
# threshold_x = data['Views'].quantile(0.99)
# threshold_y = data['Likes'].quantile(0.99)
# outliers = data[(data['Views'] > threshold_x) | (data['Likes'] > threshold_y)]
# for i in range(outliers.shape[0]):
#     plt.text(outliers['Views'].iloc[i], outliers['Likes'].iloc[i], outliers['Title'].iloc[i], fontsize=9)

# plt.legend(title='Is Short')
# plt.savefig(os.path.join(plot_dir, 'views_vs_likes.jpeg'))
# plt.close()

# # 3. Relationship between Views and Comments with v_com_ratio
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='Views', y='Comments', data=data, hue='Is Short', palette='viridis')
# plt.title('Views vs Comments')
# plt.xlabel('Views')
# plt.ylabel('Comments')

# # Annotate outliers
# threshold_x = data['Views'].quantile(0.99)
# threshold_y = data['Comments'].quantile(0.99)
# outliers = data[(data['Views'] > threshold_x) | (data['Comments'] > threshold_y)]
# for i in range(outliers.shape[0]):
#     plt.text(outliers['Views'].iloc[i], outliers['Comments'].iloc[i], outliers['Title'].iloc[i], fontsize=9)

# plt.legend(title='Is Short')
# plt.savefig(os.path.join(plot_dir, 'views_vs_comments.jpeg'))
# plt.close()

# # # 4. Distribution of v_like_ratio and v_com_ratio
# # plt.figure(figsize=(18, 5))

# # plt.subplot(1, 2, 1)
# # sns.histplot(data['v_like_ratio'].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, kde=True, color='purple')
# # plt.title('Distribution of Views/Likes Ratio')

# # plt.subplot(1, 2, 2)
# # sns.histplot(data['v_com_ratio'].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, kde=True, color='orange')
# # plt.title('Distribution of Views/Comments Ratio')

# # plt.tight_layout()
# # plt.savefig(os.path.join(plot_dir, 'distribution_v_like_v_com_ratio.jpeg'))
# # plt.close()

# # # 5. Comparison of Short vs Long Videos
# # plt.figure(figsize=(18, 10))

# # plt.subplot(2, 3, 1)
# # sns.boxplot(x='Is Short', y='Views', data=data)
# # plt.title('Views Comparison: Shorts vs Long Videos')

# # plt.subplot(2, 3, 2)
# # sns.boxplot(x='Is Short', y='Likes', data=data)
# # plt.title('Likes Comparison: Shorts vs Long Videos')

# # plt.subplot(2, 3, 3)
# # sns.boxplot(x='Is Short', y='Comments', data=data)
# # plt.title('Comments Comparison: Shorts vs Long Videos')

# # plt.subplot(2, 3, 4)
# # sns.boxplot(x='Is Short', y='v_like_ratio', data=data)
# # plt.title('Views/Likes Ratio Comparison: Shorts vs Long Videos')

# # plt.subplot(2, 3, 5)
# # sns.boxplot(x='Is Short', y='v_com_ratio', data=data)
# # plt.title('Views/Comments Ratio Comparison: Shorts vs Long Videos')

# # plt.tight_layout()
# # plt.savefig(os.path.join(plot_dir, 'comparison_shorts_long_videos.jpeg'))
# # plt.close()

# # # 6. Density plots for Views, Likes, Comments by Video Type
# # plt.figure(figsize=(18, 10))

# # plt.subplot(2, 3, 1)
# # sns.kdeplot(data=data, x='Views', hue='Is Short', fill=True)
# # plt.title('Density Plot of Views by Video Type')

# # plt.subplot(2, 3, 2)
# # sns.kdeplot(data=data, x='Likes', hue='Is Short', fill=True)
# # plt.title('Density Plot of Likes by Video Type')

# # plt.subplot(2, 3, 3)
# # sns.kdeplot(data=data, x='Comments', hue='Is Short', fill=True)
# # plt.title('Density Plot of Comments by Video Type')

# # plt.subplot(2, 3, 4)
# # sns.kdeplot(data=data, x='v_like_ratio', hue='Is Short', fill=True)
# # plt.title('Density Plot of Views/Likes Ratio by Video Type')

# # plt.subplot(2, 3, 5)
# # sns.kdeplot(data=data, x='v_com_ratio', hue='Is Short', fill=True)
# # plt.title('Density Plot of Views/Comments Ratio by Video Type')

# # plt.tight_layout()
# # plt.savefig(os.path.join(plot_dir, 'density_plots_views_likes_comments_ratios.jpeg'))
# # plt.close()


# # Encode the categorical 'Is Short' data
# le = LabelEncoder()
# data['Is Short'] = le.fit_transform(data['Is Short'])

# # 7. 3D plot for Views, Likes, and Comments with cmap='cool'
# fig = plt.figure(figsize=(12, 10))
# ax = fig.add_subplot(111, projection='3d')

# sc = ax.scatter(data['Views'], data['Likes'], data['Comments'], c=data['Is Short'], cmap='cool', s=50)
# ax.set_xlabel('Views')
# ax.set_ylabel('Likes')
# ax.set_zlabel('Comments')
# plt.title('3D Plot of Views, Likes, and Comments')
# legend1 = ax.legend(*sc.legend_elements(), title="Is Short")
# ax.add_artist(legend1)

# # Annotate outliers
# threshold_views = data['Views'].quantile(0.99)
# threshold_likes = data['Likes'].quantile(0.99)
# threshold_comments = data['Comments'].quantile(0.99)
# outliers = data[(data['Views'] > threshold_views) | (data['Likes'] > threshold_likes) | (data['Comments'] > threshold_comments)]

# for i in range(outliers.shape[0]):
#     ax.text(outliers['Views'].iloc[i], outliers['Likes'].iloc[i], outliers['Comments'].iloc[i], 
#             outliers['Title'].iloc[i], fontsize=9, color='black', weight='bold', style='italic')

# # Highlight outliers with larger points
# ax.scatter(outliers['Views'], outliers['Likes'], outliers['Comments'], c='red', s=100, edgecolor='k', label='Outliers')

# plt.savefig(os.path.join(plot_dir, '3d_plot_views_likes_comments_cool.jpeg'))
# plt.close()



# # # 8. Additional Analysis: Correlation Heatmap
# # plt.figure(figsize=(12, 8))
# # corr_matrix = data.corr()
# # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
# # plt.title('Correlation Matrix')
# # plt.savefig(os.path.join(plot_dir, 'correlation_matrix.jpeg'))
# # plt.close()

# # If there's a timestamp column, perform time series analysis
# if 'Timestamp' in data.columns:
#     data['Timestamp'] = pd.to_datetime(data['Timestamp'])
#     data.set_index('Timestamp', inplace=True)
    
#     # Resampling to monthly data
#     monthly_data = data.resample('M').sum()
    
#     plt.figure(figsize=(15, 6))
    
#     plt.subplot(2, 1, 1)
#     monthly_data['Views'].plot()
#     plt.title('Monthly Views')
    
#     plt.subplot(2, 1, 2)
#     monthly_data['Likes'].plot(label='Likes')
#     monthly_data['Comments'].plot(label='Comments')
#     plt.legend()
#     plt.title('Monthly Likes and Comments')
    
#     plt.tight_layout()
#     plt.savefig(os.path.join(plot_dir, 'monthly_views_likes.jpeg'))
#     plt.close()
    
#     plt.figure(figsize=(15, 6))
    
#     plt.subplot(2, 1, 1)
#     monthly_data['Comments'].plot()
#     plt.title('Monthly Comments')
    
#     plt.subplot(2, 1, 2)
#     monthly_data['Views'].plot(label='Views')
#     monthly_data['Likes'].plot(label='Likes')
#     monthly_data['Comments'].plot(label='Comments')
#     plt.legend()
#     plt.title('Monthly Views, Likes, and Comments')
    
#     plt.tight_layout()
#     plt.savefig(os.path.join(plot_dir, 'monthly_views_likes_comments.jpeg'))
#     plt.close()

# # Display data description
# data_description