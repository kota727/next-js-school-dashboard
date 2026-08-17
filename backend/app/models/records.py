import enum

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Exam(Base):
    """
    One exam belongs to exactly one ClassSubject (one class, one
    subject, one teacher). This is what an Excel upload targets.
    """
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    class_subject_id = Column(Integer, ForeignKey("class_subjects.id"), nullable=False)
    term = Column(String(50), nullable=False)     # "Term 1", "Midterm", etc.
    max_marks = Column(Integer, nullable=False, default=100)
    exam_date = Column(Date, nullable=True)

    class_subject = relationship("ClassSubject", back_populates="exams")
    marks = relationship("Mark", back_populates="exam")


class Mark(Base):
    """
    One row per (exam, student). This is the table the Excel parser
    bulk-inserts/upserts into — one row created per spreadsheet row.
    """
    __tablename__ = "marks"
    __table_args__ = (
        # A student can only have ONE mark entry per exam — re-uploading
        # the same sheet should update, not duplicate, this row.
        UniqueConstraint("exam_id", "student_id", name="uq_exam_student"),
    )

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    marks_obtained = Column(Float, nullable=False)
    remarks = Column(String(255), nullable=True)

    exam = relationship("Exam", back_populates="marks")
    student = relationship("Student", back_populates="marks")


class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("student_id", "date", name="uq_student_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)

    student = relationship("Student", back_populates="attendance_records")
