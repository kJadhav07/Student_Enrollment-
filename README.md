# Student Enrollment System

A beginner-friendly, menu-driven Student Enrollment System built with Python for colleges and institutes.

## Features

- Add student details: ID, name, age, mobile, email, course, and fees.
- View all enrolled students.
- Search students by Student ID.
- Update student information.
- Delete student records with confirmation.
- Enroll students in different courses.
- View total, paid, and remaining fees.
- Validate student information and fee amounts.
- Save and load records using JSON.

## Technologies Used

- Python 3
- JSON for data storage
- Object-Oriented Programming (OOP)
- Classes and objects
- Functions and methods
- Lists and dictionaries
- Loops and conditional statements
- Exception handling
- File handling

## Project Files

```text
student-enrollment
├── student_enrollment.py
```

## Requirements

- Python 3 installed
- VS Code or another Python editor

No additional packages are required.

## How to Run

1. Download or clone the project.
2. Open the project folder in VS Code.
3. Open Terminal → New Terminal.
4. Run the following command:

```bash
python student_enrollment.py
```

If needed, use:

```bash
python3 student_enrollment.py
```

## Main Menu

```text
Welcome to Student Enrollment System!

1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Enroll in Course
7. View Fee Details
8. Exit
```

## Example Output

```text
Enter Student ID: 101
Enter Student Name: Kavita Jadhav
Enter Age: 23
Enter Mobile Number: 6360686153
Enter Email: kavita@example.com
Enter Course: Python
Enter Total Fees: 10000
Enter Paid Fees: 3000

Student enrolled successfully!
Remaining Fees: ₹7000.00
```

## Data Storage

Student information is stored in `students.json` and loaded when the program starts. Keep this file in the project folder to preserve your records.

## Author

**Kavita Jadhav**

## Purpose

This project is created for educational purposes to practise Python programming, OOP, validation, and JSON file handling.
