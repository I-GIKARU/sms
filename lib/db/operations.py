from datetime import datetime
from .models import Student, Teacher, Course, ContactInfo, Enrollment
from icecream import ic


class SchoolOperations:
    def __init__(self, session):
        self.session = session

    # Add operations
    def add_student(self, name, grade):
        student = Student(name=name, grade=grade)
        self.session.add(student)
        self.session.commit()
        return student

    def add_teacher(self, name, department):
        teacher = Teacher(name=name, department=department)
        self.session.add(teacher)
        self.session.commit()
        return teacher

    def add_course(self, name, teacher_id):
        if not self.session.query(Teacher).get(teacher_id):
            raise ValueError("Teacher does not exist")
        course = Course(name=name, teacher_id=teacher_id)
        self.session.add(course)
        self.session.commit()
        return course

    def enroll_student(self, student_id, course_id):
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            enrollment_date=datetime.now()
        )
        self.session.add(enrollment)
        self.session.commit()
        return enrollment

    def add_contact_info(self, student_id, address, phone, email):
        contact = ContactInfo(
            student_id=student_id,
            address=address,
            phone=phone,
            email=email
        )
        self.session.add(contact)
        self.session.commit()
        return contact

    # Get operations
    def get_student(self, student_id):
        return self.session.query(Student).get(student_id)

    def get_teacher(self, teacher_id):
        return self.session.query(Teacher).get(teacher_id)

    def get_course(self, course_id):
        return self.session.query(Course).get(course_id)

    # Update operations
    def update_student(self, student_id, name=None, grade=None):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("Student not found")
        if name:
            student.name = name
        if grade:
            student.grade = grade
        self.session.commit()
        return student

    def update_teacher(self, teacher_id, name=None, department=None):
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")
        if name:
            teacher.name = name
        if department:
            teacher.department = department
        self.session.commit()
        return teacher

    def update_course(self, course_id, name=None, teacher_id=None):
        course = self.get_course(course_id)
        if not course:
            raise ValueError("Course not found")
        if name:
            course.name = name
        if teacher_id:
            if not self.get_teacher(teacher_id):
                raise ValueError("Teacher does not exist")
            course.teacher_id = teacher_id
        self.session.commit()
        return course

    # Delete operations
    def delete_student(self, student_id):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("Student not found")
        self.session.delete(student)
        self.session.commit()

    def delete_teacher(self, teacher_id):
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")
        self.session.delete(teacher)
        self.session.commit()

    def delete_course(self, course_id):
        course = self.get_course(course_id)
        if not course:
            raise ValueError("Course not found")

        # First delete all enrollments for this course
        self.session.query(Enrollment).filter_by(course_id=course_id).delete()

        # Then delete the course
        self.session.delete(course)
        self.session.commit()

    # List operations
    def list_all_students(self):
        return self.session.query(Student).order_by(Student.name).all()

    def list_all_teachers(self):
        return self.session.query(Teacher).order_by(Teacher.name).all()

    def list_all_courses(self):
        return self.session.query(Course).order_by(Course.name).all()

    def list_students_in_course(self, course_id):
        course = self.get_course(course_id)
        return course.students if course else []

    def list_courses_for_student(self, student_id):
        student = self.get_student(student_id)
        return student.courses if student else []

    # Detailed report
    def display_students_courses(self):
        students = self.list_all_students()
        for student in students:
            print(f"\n{student.name} (ID: {student.id}, Grade: {student.grade})")
            print("Enrolled in:")
            for enrollment in student.courses:
                course = enrollment.course
                ic(f"- {course.name} (Course ID: {course.id})")
                ic(f"  Teacher: {course.teacher.name}")
                ic(f"  Enrollment Date: {enrollment.enrollment_date}")
            ic(f"Total courses: {len(student.courses)}")