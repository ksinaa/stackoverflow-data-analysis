import pandas as pd
import sqlite3

def getUniqueSkillNames():
    skillNames = pd.read_csv('skillArea.csv')
    return skillNames['Name'].tolist()

def getAuthorHistory(author_id, selected_skills=None):
    conn = sqlite3.connect('./indexWithPython/index.db')
    query = f"SELECT posts.CreationDate, posts.Score, clusters.SkillArea FROM posts INNER JOIN clusters ON clusters.Id = posts.Id WHERE posts.PostTypeId = 2 AND posts.OwnerUserId = {author_id}"

    df = pd.read_sql_query(query, conn)

    df['SkillArea'] = df['SkillArea'].str.split(',')

    df = df.explode('SkillArea')

    # Ensure the 'CreationDate' is in datetime format
    df['CreationDate'] = pd.to_datetime(df['CreationDate'])

    # Sort by CreationDate to ensure consistency
    df = df.sort_values('CreationDate')

    skillNames = pd.read_csv('skillArea.csv')

    df = pd.merge(df, skillNames, left_on='SkillArea', right_on='SkillArea', how='left')

    conn.close()

    if selected_skills:
        df = df[df['Name'].isin(selected_skills)]

    print("Data fetched successfully")
    print(f"Number of rows: {len(df)}")

    return df['CreationDate'].tolist(), df['Score'].tolist(), df['Name'].tolist()