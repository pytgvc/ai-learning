import sqlite3

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    city TEXT,
    marks INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_courses (
    name TEXT,
    course TEXT
)
""")

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM student_courses")

students = [
    ("Asha", "Bhopal", 85),
    ("Ravi", "Indore", 90),
    ("Neha", "Delhi", 78),
    ("Aman", "Bhopal", 92),
    ("Priya", "Indore", 88),
    ("Rahul", "Delhi", 75),
    ("Sneha", "Bhopal", 95),
    ("Karan", "Delhi", 80),
    ("Pooja", "Bhopal", 83),
    ("Arjun", "Bhopal", 89)
]

cursor.executemany("""
INSERT INTO students (name, city, marks)
VALUES (?, ?, ?)
""", students)

courses = [
    ("Asha", "AI"),
    ("Ravi", "Python"),
    ("Neha", "Data Science"),
    ("Aman", "AI"),
    ("Priya", "Python"),
    ("Rahul", "Data Science"),
    ("Sneha", "AI"),
    ("Karan", "Python"),
    ("Pooja", "Data Science"),
    ("Arjun", "AI")
]

cursor.executemany("""
INSERT INTO student_courses (name, course)
VALUES (?, ?)
""", courses)

connection.commit()

print("\n--- ALL STUDENTS ---")
cursor.execute("SELECT * FROM students")
for student in cursor.fetchall():
    print(student)

print("\n--- CITY SEARCH ---")
city = input("Enter city: ").strip().title()

cursor.execute(
    "SELECT name, city, marks FROM students WHERE city = ?",
    (city,)
)

city_students = cursor.fetchall()

if city_students:
    for student in city_students:
        print(student)
    print("Total:", len(city_students))
else:
    print("No students found in", city)

print("\n--- HIGHEST MARKS ---")
cursor.execute("""
SELECT * FROM students
ORDER BY marks DESC
""")

for student in cursor.fetchall():
    print(student)

print("\n--- TOTAL STUDENTS ---")
cursor.execute("SELECT COUNT(*) FROM students")
print("Total:", cursor.fetchone()[0])

print("\n--- GROUP BY CITY ---")
cursor.execute("""
SELECT city, COUNT(*)
FROM students
GROUP BY city
ORDER BY city
""")

for city, count in cursor.fetchall():
    print(city, ":", count)

print("\n--- STUDENT COURSE DETAILS ---")
cursor.execute("""
SELECT students.name, students.city, student_courses.course
FROM students
INNER JOIN student_courses
ON students.name = student_courses.name
ORDER BY students.name
""")

for student in cursor.fetchall():
    print(student)

connection.close()