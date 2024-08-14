import pandas as pd
import sqlite3

def getAuthorHistory(author_id):
    conn = sqlite3.connect('./indexWithPython/index.db')
    query = f"SELECT posts.CreationDate, posts.Score, clusters.SkillArea FROM posts INNER JOIN clusters ON clusters.Id = posts.Id WHERE posts.PostTypeId = 2 AND posts.OwnerUserId = {author_id}"
    
    df = pd.read_sql_query(query, conn)
    print(df)
    conn.close()

    # Ensure the 'CreationDate' is in datetime format
    df['CreationDate'] = pd.to_datetime(df['CreationDate'])
    return df['CreationDate'].tolist(), df['Score'].tolist(), df['SkillArea']
