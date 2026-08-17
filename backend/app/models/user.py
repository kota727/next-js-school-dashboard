import enum

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"
    parent = "parent"


class User(Base):
    """
    One row per login. Holds credentials + role only.
    Role-specific data (roll_no, specialization, etc.) lives in the
    Student/Teacher/Parent tables below, linked by user_id.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # One-to-one links — a user has AT MOST one matching profile,
    # depending on their role.
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    parent_profile = relationship("Parent", back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    roll_no = Column(String(20), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)

    user = relationship("User", back_populates="student_profile")
    school_class = relationship("SchoolClass", back_populates="students")
    marks = relationship("Mark", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")
    parent_links = relationship("ParentStudent", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    user = relationship("User", back_populates="teacher_profile")
    class_subjects = relationship("ClassSubject", back_populates="teacher")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    user = relationship("User", back_populates="parent_profile")
    student_links = relationship("ParentStudent", back_populates="parent")


class ParentStudent(Base):
    """
    Join table: a parent can have multiple children, and (in shared
    custody / guardian cases) a student can have multiple guardians.
    """
    __tablename__ = "parent_student"

    parent_id = Column(Integer, ForeignKey("parents.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)

    parent = relationship("Parent", back_populates="student_links")
    student = relationship("Student", back_populates="parent_links")
