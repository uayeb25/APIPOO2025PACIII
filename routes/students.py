from fastapi import APIRouter, HTTPException, Request
from models.students import Student
from controllers.students import (
    create_student
)

router = APIRouter(prefix="/students")

@router.post( "/" , tags=["Students"] )
async def create_new_student(student_data: Student):
    result = await create_student(student_data)
    return result