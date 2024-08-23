import pandas as pd
import sqlite3
import numpy as np

conn = sqlite3.connect('./indexWithPython/index.db')
query = 'SELECT posts.OwnerUserId, posts.CreationDate, posts.Score, clusters.SkillArea FROM posts INNER JOIN clusters ON clusters.Id = posts.Id WHERE posts.PostTypeId = 2'

def normalize_scores(group):
    total = group.sum()
    if total == 0:
        return [1.0 / len(group)] * len(group)  # Equal distribution if sum is zero
    else:
        return group / total

df = pd.read_sql_query(query, conn)

df['SkillArea'] = df['SkillArea'].str.split(',')
df = df.explode('SkillArea')

df['CreationDate'] = pd.to_datetime(df['CreationDate'])
df = df.sort_values('CreationDate')

skillNames = pd.read_csv('skillArea.csv')
df = pd.merge(df, skillNames, left_on='SkillArea', right_on='SkillArea', how='left')

conn.close()

df = df.drop(columns='SkillArea')
df = df.rename(columns={'Name': 'SkillArea'})

df['Year'] = df['CreationDate'].dt.year

# Calculate median score
df = df.groupby(['OwnerUserId', 'Year', 'SkillArea'])['Score'].agg(median_score=lambda x: np.median(x)).reset_index()

# Sort the dataframe
df = df.sort_values(['Year', 'OwnerUserId', 'SkillArea'])

# Save median scores to CSV
df.to_csv('./median_score.csv', index=False)

# Group by OwnerUserId and Year, then apply normalization
df['normalized_score'] = df.groupby(['OwnerUserId', 'Year'])['median_score'].transform(normalize_scores)

# Sort the dataframe again
df = df.sort_values(['OwnerUserId', 'Year', 'SkillArea'])

# Display the result
print(df)

# Optionally, save the final result with normalized scores
df.to_csv('./normalized_score.csv', index=False)