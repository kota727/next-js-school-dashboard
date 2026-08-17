from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class SchoolClass(Base):
    """E.g. "Class 8", section "A" -> Class 8-A."""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)      # "Class 8"
    section = Column(String(10), nullable=True)     # "A"

    students = relationship("Student", back_populates="school_class")
    class_subjects = relationship("ClassSubject", back_populates="school_class")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)       # "Mathematics"
    code = Column(String(20), unique=True, nullable=True)  # "MATH8"

    class_subjects = relationship("ClassSubject", back_populates="subject")


class ClassSubject(Base):
    """
    The key linking table: "Teacher X teaches Subject Y to Class Z".
    This is what the Excel upload feature keys off — a teacher picks
    a ClassSubject, then uploads marks for every student in that class.
    """
    __tablename__ = "class_subjects"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    school_class = relationship("SchoolClass", back_populates="class_subjects")
    subject = relationship("Subject", back_populates="class_subjects")
    teacher = relationship("Teacher", back_populates="class_subjects")
    exams = relationship("Exam", back_populates="class_subject")
