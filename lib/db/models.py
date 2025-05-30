from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Enrollment(Base):
    __tablename__ = 'enrollments'
    student_id = Column(Integer, ForeignKey('students.id', ), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    enrollment_date = Column(Date)
    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    grade = Column(String)
    contact_info = relationship("ContactInfo", uselist=False, back_populates="student")
    courses = relationship("Enrollment", back_populates="student")

class ContactInfo(Base):
    __tablename__ = 'contact_info'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    student_id = Column(Integer, ForeignKey('students.id'), unique=True)
    student = relationship("Student", back_populates="contact_info")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)
    courses = relationship("Course", back_populates="teacher")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="courses")
    students = relationship("Enrollment", back_populates="course")