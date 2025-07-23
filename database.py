import sqlite3

# Database setup
connection=sqlite3.connect("six_nations.db")

# Create cursor
cursor=connection.cursor()

# Create the table
create_table_query="""
CREATE TABLE IF NOT EXISTS SIX_NATIONS (
    TEAM    VARCHAR(25),
    STADIUM  VARCHAR(50),
    LOCATION VARCHAR(25),
    CAPACITY   INT
);
"""

cursor.execute(create_table_query)

# Insert Records
sql_query = """INSERT INTO SIX_NATIONS (TEAM, STADIUM, LOCATION, CAPACITY) VALUES (?, ?, ?, ?)"""
values = [
    ('England', 'Twickenham Stadium', 'London', 82000),
    ('France', 'Stade de France', 'Saint-Denis', 81338),
    ('Wales', 'Principality Stadium', 'Cardiff', 73931),
    ('Italy', 'Stadio Olimpico', 'Rome', 72698),
    ('Scotland', 'Murrayfield Stadium', 'Edinburgh', 67144),
    ('Ireland', 'Aviva Stadium', 'Dublin', 51700)
]

cursor.executemany(sql_query, values)
connection.commit()

# Display the records
data=cursor.execute("""Select * from SIX_NATIONS""")

for row in data:
    print(row)

if connection:
    connection.close()