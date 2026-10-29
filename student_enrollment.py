import json
import os
import re


class Student:
    """Stores details for one student."""

    def __init__(self, student_id, name, age, mobile, email, course,
                 total_fees, paid_fees):
        self.student_id = str(student_id)
        self.name = name
        self.age = age
        self.mobile = mobile
        self.email = email
        self.course = course
        self.total_fees = float(total_fees)
        self.paid_fees = float(paid_fees)

    @property
    def remaining_fees(self):
        return self.total_fees - self.paid_fees

    def to_dict(self):
        """Convert a Student object into a dictionary for JSON."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "mobile": self.mobile,
            "email": self.email,
            "course": self.course,
            "total_fees": self.total_fees,
            "paid_fees": self.paid_fees,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Student object from saved JSON data."""
        return cls(
            data["student_id"], data["name"], data["age"], data["mobile"],
            data["email"], data["course"], data["total_fees"],
            data["paid_fees"]
        )


class EnrollmentSystem:
    """Manages student enrollment records."""

    FILE_NAME = "students.json"
    COURSES = ["Python", "Data Science", "Web Development", "SQL"]

    def __init__(self):
        self.students = {}
        self.load_data()

    def load_data(self):
        """Load student records when the program starts."""
        if not os.path.exists(self.FILE_NAME):
            self.save_data()
            return

        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.students = {
                str(item["student_id"]): Student.from_dict(item)
                for item in data
            }
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
            print(f"Warning: Could not load saved data ({error}). Starting with empty records.")
            self.students = {}

    def save_data(self):
        """Save all student records to JSON."""
        try:
            with open(self.FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in self.students.values()],
                    file,
                    indent=4
                )
        except OSError as error:
            print(f"Error saving data: {error}")

    @staticmethod
    def get_non_empty(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty. Please try again.")

    @staticmethod
    def get_integer(prompt, minimum=None):
        while True:
            try:
                value = int(input(prompt))
                if minimum is not None and value < minimum:
                    print(f"Please enter a number greater than or equal to {minimum}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid whole number.")

    @staticmethod
    def get_money(prompt):
        while True:
            try:
                value = float(input(prompt))
                if value < 0:
                    print("Amount cannot be negative.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid amount, such as 1000 or 1000.50.")

    def choose_course(self):
        print("\nAvailable Courses:")
        for number, course in enumerate(self.COURSES, start=1):
            print(f"{number}. {course}")
        choice = self.get_integer("Choose course number: ", 1)
        while choice > len(self.COURSES):
            print("Invalid course choice.")
            choice = self.get_integer("Choose course number: ", 1)
        return self.COURSES[choice - 1]

    @staticmethod
    def valid_email(email):
        return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

    @staticmethod
    def valid_mobile(mobile):
        return mobile.isdigit() and len(mobile) == 10

    def add_student(self):
        print("\n--- Add Student ---")
        student_id = self.get_non_empty("Enter Student ID: ")
        if student_id in self.students:
            print("That Student ID already exists.")
            return

        name = self.get_non_empty("Enter Student Name: ")
        age = self.get_integer("Enter Age (minimum 1): ", 1)
        mobile = self.get_non_empty("Enter 10-digit Mobile Number: ")
        while not self.valid_mobile(mobile):
            print("Please enter exactly 10 digits.")
            mobile = self.get_non_empty("Enter 10-digit Mobile Number: ")

        email = self.get_non_empty("Enter Email: ")
        while not self.valid_email(email):
            print("Please enter a valid email address.")
            email = self.get_non_empty("Enter Email: ")

        course = self.choose_course()
        total_fees = self.get_money("Enter Total Fees: ")
        paid_fees = self.get_money("Enter Paid Fees: ")
        while paid_fees > total_fees:
            print("Paid fees cannot be greater than total fees.")
            paid_fees = self.get_money("Enter Paid Fees: ")

        student = Student(
            student_id, name, age, mobile, email, course, total_fees, paid_fees
        )
        self.students[student_id] = student
        self.save_data()
        print("\nStudent enrolled successfully!")
        print(f"Remaining Fees: ₹{student.remaining_fees:.2f}")

    def display_student(self, student):
        print("\n------------------------------")
        print(f"Student ID      : {student.student_id}")
        print(f"Name            : {student.name}")
        print(f"Age             : {student.age}")
        print(f"Mobile          : {student.mobile}")
        print(f"Email           : {student.email}")
        print(f"Course          : {student.course}")
        print(f"Total Fees      : ₹{student.total_fees:.2f}")
        print(f"Paid Fees       : ₹{student.paid_fees:.2f}")
        print(f"Remaining Fees  : ₹{student.remaining_fees:.2f}")
        print("------------------------------")

    def view_students(self):
        print("\n--- All Enrolled Students ---")
        if not self.students:
            print("No student records found.")
            return
        for student in self.students.values():
            self.display_student(student)

    def search_student(self):
        student_id = self.get_non_empty("Enter Student ID to search: ")
        student = self.students.get(student_id)
        if student:
            self.display_student(student)
        else:
            print("Student not found.")

    def update_student(self):
        student_id = self.get_non_empty("Enter Student ID to update: ")
        student = self.students.get(student_id)
        if not student:
            print("Student not found.")
            return

        while True:
            print("\nWhat would you like to update?")
            print("1. Name")
            print("2. Age")
            print("3. Mobile Number")
            print("4. Email")
            print("5. Course")
            print("6. Back to Main Menu")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                student.name = self.get_non_empty("Enter new name: ")
            elif choice == "2":
                student.age = self.get_integer("Enter new age: ", 1)
            elif choice == "3":
                mobile = self.get_non_empty("Enter new 10-digit mobile: ")
                while not self.valid_mobile(mobile):
                    print("Please enter exactly 10 digits.")
                    mobile = self.get_non_empty("Enter new 10-digit mobile: ")
                student.mobile = mobile
            elif choice == "4":
                email = self.get_non_empty("Enter new email: ")
                while not self.valid_email(email):
                    print("Please enter a valid email address.")
                    email = self.get_non_empty("Enter new email: ")
                student.email = email
            elif choice == "5":
                student.course = self.choose_course()
            elif choice == "6":
                break
            else:
                print("Invalid choice.")
                continue

            self.save_data()
            print("Student details updated successfully.")

    def delete_student(self):
        student_id = self.get_non_empty("Enter Student ID to delete: ")
        if student_id not in self.students:
            print("Student not found.")
            return
        confirm = input("Are you sure you want to delete this student? (yes/no): ").strip().lower()
        if confirm == "yes":
            del self.students[student_id]
            self.save_data()
            print("Student deleted successfully.")
        else:
            print("Deletion cancelled.")

    def enroll_course(self):
        student_id = self.get_non_empty("Enter Student ID: ")
        student = self.students.get(student_id)
        if not student:
            print("Student not found.")
            return
        print(f"Current course: {student.course}")
        student.course = self.choose_course()
        self.save_data()
        print(f"Course updated to {student.course} successfully.")

    def view_fees(self):
        student_id = self.get_non_empty("Enter Student ID: ")
        student = self.students.get(student_id)
        if not student:
            print("Student not found.")
            return
        print(f"\nStudent Name   : {student.name}")
        print(f"Total Fees     : ₹{student.total_fees:.2f}")
        print(f"Paid Fees      : ₹{student.paid_fees:.2f}")
        print(f"Remaining Fees : ₹{student.remaining_fees:.2f}")

    def run(self):
        print("\nWelcome to Student Enrollment System!")
        while True:
            print("\n========== MAIN MENU ==========")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Enroll in Course")
            print("7. View Fee Details")
            print("8. Exit")
            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self.add_student()
                elif choice == "2":
                    self.view_students()
                elif choice == "3":
                    self.search_student()
                elif choice == "4":
                    self.update_student()
                elif choice == "5":
                    self.delete_student()
                elif choice == "6":
                    self.enroll_course()
                elif choice == "7":
                    self.view_fees()
                elif choice == "8":
                    print("Thank you for using Student Enrollment System. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please select 1 to 8.")
            except (KeyboardInterrupt, EOFError):
                print("\nInput cancelled. Returning to main menu.")
            except Exception as error:
                print(f"Something went wrong: {error}")


if __name__ == "__main__":
    system = EnrollmentSystem()
    system.run()
