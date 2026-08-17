# School management system — project documentation

This file is a running log of what was built, why, and what went wrong
along the way. Kept for learning purposes and as a reference (e.g. for
explaining project challenges in interviews).

---

## 1. Project overview

A full-stack school management web app with four roles — student,
teacher, parent, admin — each with a distinct dashboard and permissions.

**Stack**
- Frontend: Next.js 15 (App Router) + Tailwind CSS
- Backend: FastAPI (Python)
- Database: MySQL, accessed via SQLAlchemy ORM
- Auth: JWT with a role claim, checked on both frontend (route guards)
  and backend (dependency-based middleware)

**Key feature driving the design:** teachers should never have to enter
marks one student at a time. They upload an Excel sheet for a class +
subject, and the backend parses and bulk-inserts marks for every
student in that sheet (using pandas/openpyxl).

---

## 2. Database schema — decisions and reasoning

### Why separate role tables instead of one big `users` table?

We could have put every possible field (roll_no, specialization, phone,
etc.) directly on `users`. We didn't, because:
- Most columns would be NULL for most rows (a student has no
  `specialization`, a teacher has no `roll_no`) — wasteful and messy.
- Each role's data model can evolve independently without touching the
  auth table.

Instead: `users` holds only login/auth data + a `role` enum. Each role
gets its own profile table (`students`, `teachers`, `parents`) linked
back via a `user_id` foreign key (one-to-one).

### Why a `parent_student` join table instead of a direct FK?

A student can have more than one parent/guardian, and a parent can have
more than one child. That's a many-to-many relationship, which requires
a join table rather than a foreign key on either side.

### Why `class_subjects` as its own table?

This table answers "who teaches what to which class" — it's the pivot
that the Excel upload feature keys off. A teacher picks a `ClassSubject`
(e.g. "Class 8-A, Mathematics"), and the upload targets every student
enrolled in that class.

### Why a `UniqueConstraint` on `marks (exam_id, student_id)`?

Teachers will re-upload corrected sheets. Without this constraint,
re-uploading would create duplicate mark rows per student. With it, the
upload logic can "upsert" — insert if new, update if it already exists.

### Full schema

See the ERD shared in conversation (11 tables: `users`, `students`,
`teachers`, `parents`, `parent_student`, `classes`, `subjects`,
`class_subjects`, `exams`, `marks`, `attendance`).

---

## 3. Backend scaffold (FastAPI)

```
backend/
├── app/
│   ├── main.py            # FastAPI entrypoint, /health route
│   ├── core/
│   │   ├── config.py       # env-driven settings (DB creds, JWT secret)
│   │   └── database.py     # SQLAlchemy engine, session, get_db()
│   └── models/
│       ├── user.py         # User, Student, Teacher, Parent, ParentStudent
│       ├── academic.py     # SchoolClass, Subject, ClassSubject
│       └── records.py      # Exam, Mark, Attendance
├── requirements.txt
└── .env.example
```

`get_db()` is a FastAPI dependency: it's injected into route functions
via `Depends(get_db)`. FastAPI calls it before the route runs, hands the
route the yielded `Session`, then always runs `db.close()` afterwards —
even on error — via the `finally` block. This guarantees every request
gets an isolated, cleaned-up DB session.

`Base.metadata.create_all()` (called on FastAPI startup) is fine for
development — it creates tables that don't exist yet — but it does NOT
handle schema changes to existing tables (e.g. adding a column later).
For that we'll eventually want Alembic migrations.

---

## 4. Issues encountered

| # | Issue | Cause | Fix |
|---|-------|-------|-----|
| 1 | `ModuleNotFoundError: No module named 'mysql'` when creating the SQLAlchemy engine | `mysql-connector-python` (the MySQL driver SQLAlchemy needs) wasn't installed yet — SQLAlchemy's `mysql+mysqlconnector://` URL scheme requires it | Installed `mysql-connector-python` via pip |

*(more entries added here as we hit issues)*

---

## 5. Next steps

- [ ] Create local MySQL database (`school_db`)
- [ ] Generate real tables in MySQL from the SQLAlchemy models
- [ ] Learn joins/views/indexes/query optimization as we query this schema
- [ ] Build JWT auth (login endpoint, password hashing, role-based dependency)
- [ ] Excel upload endpoint for marks
- [ ] PDF report generation
- [ ] Next.js dashboards per role
