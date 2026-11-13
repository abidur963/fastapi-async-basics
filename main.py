
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Student Management API",
    description="My first FastAPI learning project",
    version="1.0.0"
)

# Student data model
class Student(BaseModel):
    id: int
    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
    department: str


# Temporary student database
students = [
    {"id": 1, "name": "Amina", "age": 21, "department": "CSE"},
    {"id": 2, "name": "Rahim", "age": 22, "department": "EEE"},
    {"id": 3, "name": "Nadia", "age": 20, "department": "CSE"}
]


# 1. Home endpoint
@app.get("/")
async def home():
    return {"message": "Welcome to Student Management API"}


# 2. Get all students (Query Parameters)
@app.get("/students")
async def get_students(
    department: Optional[str] = None,
    min_age: Optional[int] = None
):
    result = students

    if department:
        result = [
            s for s in result
            if s["department"].lower() == department.lower()
        ]

    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]

    return {"count": len(result), "students": result}


# 3. Get one student (Path Parameter)
@app.get("/students/{student_id}")
async def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


# 4. Create a student (POST)
@app.post("/students", status_code=201)
async def create_student(student: Student):
    if any(s["id"] == student.id for s in students):
        raise HTTPException(
            status_code=409,
            detail="Student ID already exists"
        )

    new_student = student.model_dump()
    students.append(new_student)

    return {
        "message": "Student created successfully",
        "student": new_student
    }


# 5. Async example
@app.get("/about-async")
async def about_async():
    return {
        "concept": "async/await",
        "message": "This is an asynchronous endpoint"
    }


# 6. Synchronous example
@app.get("/health")
def health_check():
    return {"status": "ok"}
