import sqlite3
import logging
from lxml import etree

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the path to your large XML file
xml_file_path = '../data/Posts.xml'

# Define the fields you want to index
fields_to_index = ["Id", "PostTypeId", "CreationDate", "Score", "ViewCount", "OwnerUserId", "Title", "Tags"]

# Initialize SQLite database
conn = sqlite3.connect('index.db')
cursor = conn.cursor()

# Create table for indexing
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    Id INTEGER PRIMARY KEY,
    PostTypeId INTEGER,
    CreationDate TEXT,
    Score INTEGER,
    ViewCount INTEGER,
    OwnerUserId INTEGER,
    Title TEXT,
    Tags TEXT
)
''')

conn.commit()

# Function to insert data into SQLite in chunks
def insert_into_db(data_chunk):
    cursor.executemany('''
    INSERT OR REPLACE INTO posts (Id, PostTypeId, CreationDate, Score, ViewCount, OwnerUserId, Title, Tags)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data_chunk)
    conn.commit()
    logger.info(f"Inserted {len(data_chunk)} rows")

# Stream through the XML file and extract required fields
context = etree.iterparse(xml_file_path, events=("end",), tag="row")

data_chunk = []
chunk_size = 10000  # Define the chunk size

for event, elem in context:
    data = (
        elem.get("Id"),
        elem.get("PostTypeId"),
        elem.get("CreationDate"),
        elem.get("Score"),
        elem.get("ViewCount"),
        elem.get("OwnerUserId"),
        elem.get("Title"),
        elem.get("Tags")
    )
    data_chunk.append(data)
    
    # Insert in chunks
    if len(data_chunk) >= chunk_size:
        insert_into_db(data_chunk)
        data_chunk = []  # Reset chunk

    elem.clear()

# Insert any remaining data
if data_chunk:
    insert_into_db(data_chunk)

# Close the database connection
conn.close()
