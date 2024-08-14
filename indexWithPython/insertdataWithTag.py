from lxml import etree

# Path to your XML file
file_path = '/Users/sina/projects/uni/tshaped-Mining/files/Golden/java/JavaAnswers.xml'

# Parse the XML file with lxml
parser = etree.XMLParser(recover=True)
tree = etree.parse(file_path, parser)
root = tree.getroot()

# Extract data from the XML
posts = []
for row in root.findall('row'):
    post_id = row.get('Id')
    owner_user_id = row.get('OwnerUserId')
    parent_id = row.get('ParentId')
    accepted_answer = row.get('AcceptedAnswer')
    skill_area = row.get('SkillArea')
    posts.append((post_id, owner_user_id, parent_id, accepted_answer, skill_area))

# Connect to the SQLite database (or create it if it doesn't exist)
import sqlite3

conn = sqlite3.connect('./index.db')
cursor = conn.cursor()

# Create a table to store the posts data
cursor.execute('''
CREATE TABLE IF NOT EXISTS clusters (
    Id INTEGER PRIMARY KEY,
    OwnerUserId INTEGER,
    ParentId INTEGER,
    AcceptedAnswer INTEGER,
    SkillArea TEXT
)
''')

conn.commit()

# Insert data into the table one by one and continue if any line fails
for post in posts:
    try:
        cursor.execute('''
        INSERT INTO clusters (Id, OwnerUserId, ParentId, AcceptedAnswer, SkillArea)
        VALUES (?, ?, ?, ?, ?)
        ''', post)
        conn.commit()
    except Exception as e:
        print(f"Failed to insert record {post}: {e}")

# Close the connection
conn.close()
