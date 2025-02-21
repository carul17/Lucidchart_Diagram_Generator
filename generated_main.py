import os
import json
import zipfile
import requests
from dotenv import load_dotenv
import uuid
import re
from script import *

def main():
    print("🛠️ Generating University Course Registration System DFD and ERD...")

    # ✅ **STEP 1: CREATE DATA FLOW DIAGRAM (DFD)**
    # External Entities
    student = create_flowchart_element("Student", x=100, y=100, flowchart_type="terminator")
    faculty = create_flowchart_element("Faculty", x=100, y=300, flowchart_type="terminator")
    registrar = create_flowchart_element("Registrar's Office", x=100, y=500, flowchart_type="terminator")
    system = create_flowchart_element("Course Registration System", x=400, y=300, flowchart_type="process")
    database = create_flowchart_element("Course Database", x=700, y=300, flowchart_type="database")

    # Data Flow Lines
    create_line(student, system, "Registers for Courses", "one-to-one", start_side="right", end_side="left")
    create_line(faculty, system, "Views Enrolled Students", "one-to-one", start_side="right", end_side="left")
    create_line(system, database, "Updates Enrollment Data", "one-to-one", start_side="right", end_side="left")
    create_line(database, system, "Fetches Course Info", "one-to-one", start_side="left", end_side="right")
    create_line(system, student, "Sends Enrollment Status", "one-to-one", start_side="left", end_side="right")
    create_line(system, faculty, "Assigns Grades", "one-to-one", start_side="left", end_side="right")
    create_line(registrar, system, "Requests Reports", "one-to-one", start_side="right", end_side="left")
    create_line(system, registrar, "Generates Reports", "one-to-one", start_side="left", end_side="right")

    # ✅ **STEP 2: CREATE ENTITY RELATIONSHIP DIAGRAM (ERD)**
    # Entities (Tables)
    students_table = create_entity("Students", [
        ("StudentID", True),  # Primary Key
        ("Name", False),
        ("Email", False),
        ("Major", False)
    ], x=100, y=700)

    courses_table = create_entity("Courses", [
        ("CourseID", True),  # Primary Key
        ("CourseName", False),
        ("Credits", False),
        ("FacultyID", False)
    ], x=400, y=700)

    enrollments_table = create_entity("Enrollments", [
        ("EnrollmentID", True),  # Primary Key
        ("StudentID", False),
        ("CourseID", False),
        ("Grade", False)
    ], x=250, y=900)

    faculty_table = create_entity("Faculty", [
        ("FacultyID", True),  # Primary Key
        ("Name", False),
        ("Department", False)
    ], x=700, y=700)

    # Relationships (Crow's Foot Notation)
    create_line(students_table, enrollments_table, "enrolls in", "one-to-many", start_side="right", end_side="left")  # One Student enrolls in Many Enrollments
    create_line(courses_table, enrollments_table, "associated with", "one-to-many", start_side="right", end_side="left")  # One Course associated with Many Enrollments
    create_line(faculty_table, courses_table, "teaches", "one-to-many", start_side="left", end_side="right")  # One Faculty teaches Many Courses

    # ✅ **STEP 3: IMPORT TO LUCIDCHART**
    document_id = import_to_lucidchart()

    if document_id:
        print(f"🌍 Open the Lucidchart University Course Registration System DFD + ERD: https://lucid.app/lucidchart/{document_id}/edit")

if __name__ == "__main__":
    main()