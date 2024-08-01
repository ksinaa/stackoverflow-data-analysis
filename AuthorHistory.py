import pandas as pd
import sqlite3

def getAuthorHistory(author_id):
    conn = sqlite3.connect('./indexWithPython/index.db')
    query = f"SELECT CreationDate, Score FROM posts WHERE PostTypeId = 2 AND OwnerUserId = {author_id}"
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Ensure the 'CreationDate' is in datetime format
    df['CreationDate'] = pd.to_datetime(df['CreationDate'])

    return df['CreationDate'].tolist(), df['Score'].tolist()
