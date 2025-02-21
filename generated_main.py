import webbrowser
from script import *

def main():
    print("🛠️ Generating Data Flow Diagram (DFD) and Entity Relationship Diagram (ERD)...")

    # ✅ **STEP 1: CREATE DATA FLOW DIAGRAM (DFD)**
    # External Entities
    student = create_flowchart_element("Student", x=100, y=100, flowchart_type="terminator")
    faculty = create_flowchart_element("Faculty", x=100, y=300, flowchart_type="terminator")
    system = create_flowchart_element("Course Registration System", x=400, y=200, flowchart_type="process")
    courses_db = create_flowchart_element("Courses DB", x=700, y=200, flowchart_type="database")

    # Data Flow Lines
    create_line(student, system, "Registers for Courses", "one-to-one", start_side="right", end_side="left")
    create_line(system, courses_db, "Fetches Courses", "one-to-one", start_side="right", end_side="left")
    create_line(faculty, system, "Assigns Grades", "one-to-one", start_side="right", end_side="left")
    create_line(system, student, "Provides Enrollment Status", "one-to-one", start_side="left", end_side="right")

    # ✅ **STEP 2: CREATE ENTITY RELATIONSHIP DIAGRAM (ERD)**
    # Entities (Tables)
    students_table = create_entity("Students", [
        ("StudentID", True),  # Primary Key
        ("Name", False),
        ("Email", False),
        ("Major", False)
    ], x=100, y=500)

    faculty_table = create_entity("Faculty", [
        ("FacultyID", True),  # Primary Key
        ("Name", False),
        ("Email", False),
        ("Department", False)
    ], x=400, y=500)

    courses_table = create_entity("Courses", [
        ("CourseID", True),  # Primary Key
        ("CourseName", False),
        ("Credits", False)
    ], x=700, y=500)

    enrollments_table = create_entity("Enrollments", [
        ("EnrollmentID", True),  # Primary Key
        ("StudentID", False),
        ("CourseID", False),
        ("Grade", False)
    ], x=400, y=700)

    # Relationships (Crow's Foot Notation)
    create_line(students_table, enrollments_table, "enrolls in", "one-to-many", start_side="right", end_side="left")
    create_line(courses_table, enrollments_table, "available for", "one-to-many", start_side="bottom", end_side="top")
    create_line(faculty_table, courses_table, "teaches", "one-to-many", start_side="right", end_side="left")

    # ✅ **STEP 3: IMPORT TO LUCIDCHART**
    document_id = import_to_lucidchart()

    if document_id:
        chart_url = f"https://lucid.app/lucidchart/{document_id}/edit"
        print(f"🌍 Open the Lucidchart DFD + ERD: {chart_url}")
        webbrowser.open(chart_url)

if __name__ == "__main__":
    main()