# Importing every model module here ensures SQLAlchemy's Base.metadata
# knows about ALL tables before create_all() is called anywhere.
# Without this, tables defined in files that are never imported would
# silently not get created.

from app.models.user import User, Student, Teacher, Parent, ParentStudent, RoleEnum
from app.models.academic import SchoolClass, Subject, ClassSubject
from app.models.records import Exam, Mark, Attendance, AttendanceStatus
