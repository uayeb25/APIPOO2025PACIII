from fastapi import APIRouter, status
from models.students import Student
from controllers.students import (
    create_student
    , update_student
    , delete_student
    , get_all
    , get_one
)

router = APIRouter(prefix="/students")


@router.get( "/" , tags=["Students"], status_code=status.HTTP_200_OK )
async def get_all_students():
    result = await get_all()
    return result

@router.post( "/" , tags=["Students"], status_code=status.HTTP_201_CREATED )
async def create_new_student(student_data: Student):
    result = await create_student(student_data)
    return result

@router.put("/{id}", tags=["Students"], status_code=status.HTTP_201_CREATED)
async def update_student_information( student_data: Student , id: int ):
    student_data.id = id
    result = await update_student(student_data)
    return result

@router.delete("/{id}", tags=["Students"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_content( id: int ):
    status: str =  await delete_student(id)
    return status

@router.get("/{id}", tags=["Students"], status_code=status.HTTP_200_OK)
async def get_one_student( id: int ):
    result: Student =  await get_one(id)
    return result