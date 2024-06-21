import sqlite3
def clear_data():
    # Ask the user if they want to clear the data
    confirm = input("Are you sure you want to clear all data? This operation is irreversible. (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Clear all data from the user table
    cursor.execute('DELETE FROM user')

    # Clear all data from the student table
    cursor.execute('DELETE FROM student')

    # Clear all data from the score table
    cursor.execute('DELETE FROM score')
    
    cursor.execute('DELETE FROM absence')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("All data has been cleared.")
clear_data()
# Connect to the SQLite database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Query all users from the user table
cursor.execute('SELECT * FROM user')
users = cursor.fetchall()

# Print all users
print("Users:")
for user in users:
    print(user)

# Query all students from the student table
cursor.execute('SELECT * FROM student')
students = cursor.fetchall()

# Print all students
print("Students:")
for student in students:
    print(student)

# Query all scores from the score table
cursor.execute('SELECT * FROM score')
scores = cursor.fetchall()

# Print all scores
print("Scores:")
for score in scores:
    print(score)

cursor.execute('SELECT * FROM absence')
absences = cursor.fetchall()

# Print all absences
print("Absences:")
for absense in absences:
    print(absense)


# Close the connection to the database
conn.close()