#lib/cli.py
from icecream import ic
from db import init_db, get_session, SchoolOperations


def display_menu():
    print("\nSchool Management System")
    print(f"{'1. Add Student':<40}{'2. Add Teacher':<40}{'3. Add Course'}")
    print(f"{'4. Enroll Student in Course':<40}{'5. Add Contact Info for Student':<40}{'6. View Students in Course'}")
    print(f"{'7. View All Students':<40}{'8. View Courses for Student':<40}{'9. View All Teachers'}")
    print(f"{'10. View All Courses':<40}{'11. View Students & Their Courses':<40}{'12. Update Student'}")
    print(f"{'13. Update Teacher':<40}{'14. Update Course':<40}{'15. Delete Student'}")
    print(f"{'16. Delete Teacher':<40}{'17. Delete Course':<40}{'18. Exit'}")
    return input("\nEnter your choice (1-18): ")


def main():
    engine = init_db()
    session = get_session(engine)
    ops = SchoolOperations(session)

    while True:
        choice = display_menu()
        if choice == '1':
            name = input("Enter student name: ")
            grade = input("Enter student grade: ")
            student = ops.add_student(name, grade)
            ic(f"Added student with ID: {student.id}")

        elif choice == '2':
            name = input("Enter teacher name: ")
            department = input("Enter department: ")
            teacher = ops.add_teacher(name, department)
            ic(f"Added teacher with ID: {teacher.id}")

        elif choice == '3':
            name = input("Enter course name: ")
            teacher_id = int(input("Enter teacher ID: "))
            course = ops.add_course(name, teacher_id)
            ic(f"Added course with ID: {course.id}")

        elif choice == '4':
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))
            enrollment = ops.enroll_student(student_id, course_id)
            ic(f"Enrolled student {student_id} in course {course_id}")

        elif choice == '5':
            student_id = int(input("Enter student ID: "))
            address = input("Enter address: ")
            phone = input("Enter phone: ")
            email = input("Enter email: ")
            contact = ops.add_contact_info(student_id, address, phone, email)
            ic(f"Added contact info for student {student_id}")

        elif choice == '6':
            course_id = int(input("Enter course ID: "))
            enrollments = ops.list_students_in_course(course_id)
            if not enrollments:
                ic(f"No students found in course {course_id}")
            else:
                ic(f"Students in course {course_id}:")
                for e in enrollments:
                    student = e.student
                    ic(f"{student.id}: {student.name} | Grade: {student.grade}")

        elif choice == '7':
            students = ops.list_all_students()
            if not students:
                ic("No students found")
            else:
                ic("All Students:")
                for s in students:
                    ic(f"{s.id}: {s.name} | Grade: {s.grade}")

        elif choice == '8':
            student_id = int(input("Enter student ID: "))
            enrollments = ops.list_courses_for_student(student_id)
            if not enrollments:
                ic(f"No courses found for student {student_id}")
            else:
                ic(f"Courses for student {student_id}:")
                for e in enrollments:
                    course = e.course
                    ic(f"{course.id}: {course.name} | Teacher: {course.teacher.name}")

        elif choice == '9':
            teachers = ops.list_all_teachers()
            if not teachers:
                ic("No teachers found")
            else:
                ic("All Teachers:")
                for t in teachers:
                    ic(f"{t.id}: {t.name} | Department: {t.department}")

        elif choice == '10':
            courses = ops.list_all_courses()
            if not courses:
                ic("No courses found")
            else:
                ic("All Courses:")
                for c in courses:
                    ic(f"{c.id}: {c.name} | Teacher: {c.teacher.name}")

        elif choice == '11':
            ops.display_students_courses()

        elif choice == '12':
            student_id = int(input("Enter student ID: "))
            name = input("Enter new name (leave blank to keep current): ")
            grade = input("Enter new grade (leave blank to keep current): ")
            student = ops.update_student(student_id, name if name else None, grade if grade else None)
            ic(f"Updated student {student_id}")

        elif choice == '13':
            teacher_id = int(input("Enter teacher ID: "))
            name = input("Enter new name (leave blank to keep current): ")
            department = input("Enter new department (leave blank to keep current): ")
            teacher = ops.update_teacher(teacher_id, name if name else None, department if department else None)
            ic(f"Updated teacher {teacher_id}")

        elif choice == '14':
            course_id = int(input("Enter course ID: "))
            name = input("Enter new name (leave blank to keep current): ")
            teacher_id = input("Enter new teacher ID (leave blank to keep current): ")
            course = ops.update_course(course_id, name if name else None, int(teacher_id) if teacher_id else None)
            ic(f"Updated course {course_id}")

        elif choice == '15':
            student_id = int(input("Enter student ID to delete: "))
            ops.delete_student(student_id)
            ic(f"Deleted student {student_id}")

        elif choice == '16':
            teacher_id = int(input("Enter teacher ID to delete: "))
            ops.delete_teacher(teacher_id)
            ic(f"Deleted teacher {teacher_id}")

        elif choice == '17':
            course_id = int(input("Enter course ID to delete: "))
            ops.delete_course(course_id)
            ic(f"Deleted course {course_id}")

        elif choice == '18':
            ic("Exiting...")
            break

        else:
            ic("Invalid choice! Please enter a number between 1-18")


if __name__ == "__main__":
    main()
