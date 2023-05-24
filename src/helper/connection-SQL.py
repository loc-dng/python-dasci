import mysql.connector

# Establish a connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    database="Learn_SQL_Python", # name of schema in db, not name of MYSQL_DATABASE
    user='root',
    password="password"
)

print("connection succeeded!")

# Create a cursor
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS sample_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    email VARCHAR(100)
)
"""
cursor.execute(create_table_query)

# Insert sample data into the table
insert_data_query = """
INSERT INTO sample_table (name, age, email)
VALUES (%s, %s, %s)
"""
sample_data = [
    ("John Doe", 25, "johndoe@example.com"),
    ("Jane Smith", 30, "janesmith@example.com"),
    ("Mike Johnson", 35, "mikejohnson@example.com")
]
cursor.executemany(insert_data_query, sample_data)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()