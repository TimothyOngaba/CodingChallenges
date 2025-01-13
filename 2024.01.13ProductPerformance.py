# importing required libraries
import pandas as pd 
import chardet
import datetime
import matplotlib.pyplot as plt
import seaborn as sns



#reading in file to create dataframe
#finding the encoding of the file
with open('/home/tim/Documents/UAEPlacement./CodingChallenges/Product_performance.txt', 'rb') as file:
    rawdata = file.read(1000)
    result = chardet.detect(rawdata)
    print(result)
# File path
file_path = '/home/tim/Documents/UAEPlacement/CodingChallenges/Product_performance.txt'
# Reading in file with UTF-16 encoding
df = pd.read_csv(file_path, delimiter='\t', encoding='utf-16')

# Sneak peak of the data
print(df.head)
print(df.dtypes)
# Converting the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
# Convert the 'Time' column to time
df['Time'] = df['Time'].apply(lambda x: x.strftime('%H:%M') + ':00' if isinstance(x, datetime.time) else x + ':00' if len(x.split(':')) == 2 else x)
# Convert to datetime directly (not just to time)
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
# Convert replies and respondents columns to integer 
columns_to_convert = ['Replies', 'Respondents'] 
for col in columns_to_convert:
    df[col] = df[col].astype(int)
print(df.dtypes)

# storing this dataframe in a csv file 
df.to_csv('Product_performance.csv', 
				index = None) 



#Creating a bar plot for category, secondary category and replies
import matplotlib.pyplot as plt
import seaborn as sns

# Summarizing the data by 'Category' and 'Secondary_category'
category_responses = df.groupby(['Category', 'Secondary_category'])['Replies'].sum().reset_index()

# Creating a bar plot
plt.figure(figsize=(12, 8))
sns.barplot(data=category_responses, x='Category', y='Replies', hue='Secondary_category', palette='viridis')

# Adding labels and title
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Replies', fontsize=12)
plt.title('Total Replies by Category and Subcategory', fontsize=15)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Annotating each bar with the number of replies
for bar in plt.gca().patches:
    height = bar.get_height()
    if height > 0:  # Only annotate if the bar height is greater than 0
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X position
            height + 0.5,                      # Y position (slightly above the bar)
            f'{int(height)}',                  # Text to display
            ha='center', va='bottom', fontsize=10, color='black'
        )

plt.tight_layout()
plt.legend(title='Subcategory', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()



import matplotlib.pyplot as plt
import numpy as np

# Summarising the data by 'Category'
category_summary = df.groupby('Category')[['Replies', 'Respondents']].sum().reset_index()

# Create positions for the bars
x = np.arange(len(category_summary['Category']))  # the label locations
width = 0.35  #width of the bars

# Creating the plot
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, category_summary['Replies'], width, label='Replies', color='skyblue')
bars2 = ax.bar(x + width/2, category_summary['Respondents'], width, label='Respondents', color='lightgreen')

# Adding labels, title, and legend
ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Replies and Respondents by Category', fontsize=15)
ax.set_xticks(x)
ax.set_xticklabels(category_summary['Category'], rotation=45, ha='right', fontsize=10)
ax.legend()

# Adding value labels to bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

plt.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensuring cottent 'Date' asdatetime format
df['Date'] = pd.to_datetime(df['Date'])

# Adding a Quarter column
df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)

# Convert 'Time' to datetime and create Time of Day categories
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
df['Time_of_Day'] = pd.cut(
    df['Time'],
    bins=[0, 6, 12, 18, 24],  # Define time ranges
    labels=['Night', 'Morning', 'Afternoon', 'Evening'],
    right=False,
    include_lowest=True
)
# Grouping data by Quarter and Time of Day and count Replies
summary = df.groupby(['Quarter', 'Time_of_Day'])['Replies'].sum().unstack()

print(summary)  # Check the summarized data

# Plotting the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(summary, annot=True, fmt='.0f', cmap='YlGnBu', cbar_kws={'label': 'Total Replies'})
plt.title('Replies by Quarter and Time of Day', fontsize=15)
plt.xlabel('Time of Day', fontsize=12)
plt.ylabel('Quarter', fontsize=12)
plt.tight_layout()
plt.show()


#looking at categories, number of replies and respondents
import matplotlib.pyplot as plt
import numpy as np

# Verifying the data
print(category_summary)

# Checking bar values
print("Replies:", category_summary['Replies'].tolist())
print("Respondents:", category_summary['Respondents'].tolist())

# Creating positions for the bars
x = np.arange(len(category_summary['Category']))  # the label locations
print("Bar positions:", x)

width = 0.35  # width of the bars

# Creating the plot
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, category_summary['Replies'], width, label='Replies', color='skyblue')
bars2 = ax.bar(x + width/2, category_summary['Respondents'], width, label='Respondents', color='lightgreen')

# Adding labels, title, and legend
ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Replies and Respondents by Category', fontsize=15)
ax.set_xticks(x)
ax.set_xticklabels(category_summary['Category'], rotation=45, ha='right', fontsize=10)
ax.legend()

# Adding value labels to bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

plt.tight_layout()
plt.savefig('debug_plot.png')  # Save for debugging
plt.show()



