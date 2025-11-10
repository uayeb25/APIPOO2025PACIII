from fastapi import APIRouter, status

from models.students import Student
from models.student_carrers import StudentCareer

from controllers.students import (
    create_student
    , update_student
    , delete_student
    , get_all
    , get_one
    , add_career
    , get_all_careers
    , get_one_career
    , remove_career
    , update_career_info
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

#### INTERACTION WITH CAREERS ####

@router.post("/{id}/careers", tags=["Students"], status_code=status.HTTP_201_CREATED)
async def assign_career_to_student( id: int, career_data: StudentCareer ):
    result = await add_career(id, career_data.career_id)
    return result

@router.get("/{id}/careers", tags=["Students"], status_code=status.HTTP_200_OK)
async def get_all_careers_of_student( id: int ):
    result = await get_all_careers(id)
    return result

@router.get("/{id}/careers/{career_id}", tags=["Students"], status_code=status.HTTP_200_OK)
async def get_one_career_of_student( id: int, career_id: int ):
    result = await get_one_career(id, career_id)
    return result

@router.delete("/{id}/careers/{career_id}", tags=["Students"], status_code=status.HTTP_204_NO_CONTENT)
async def remove_career_of_student( id: int, career_id: int ):
    status: str =  await remove_career(id, career_id)
    return status

@router.put("/{id}/careers/{career_id}", tags=["Students"], status_code=status.HTTP_201_CREATED)
async def update_career_of_student( id: int, career_id: int, career_data: StudentCareer ):
    career_data.student_id = id
    career_data.career_id = career_id
    result = await update_career_info(career_data)
    return result
