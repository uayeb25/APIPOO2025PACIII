from datetime import datetime
import json
import logging

from fastapi import HTTPException

from models.students import Student
from models.student_carrers import StudentCareer
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def get_one( id: int ) -> Student:

    selectscript = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[idperson]
            ,[email]
            ,[age]
        FROM [academics].[students]
        WHERE id = ?
    """

    params = [id]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"student not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")


async def get_all() -> list[Student]:

    selectscript = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[idperson]
            ,[email]
            ,[age]
        FROM [academics].[students]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def delete_student( id: int ) -> str:

    deletescript = """
        DELETE FROM [academics].[students]
        WHERE [id] = ?;
    """

    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def update_student( student: Student ) -> Student:

    dict = student.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [academics].[students]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( student.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    sqlfind: str = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[idperson]
            ,[email]
            ,[age]
        FROM [academics].[students]
        WHERE id = ?;
    """

    params = [student.id]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def create_student( student: Student ) -> Student:

    sqlscript: str = """
        INSERT INTO [academics].[students] ([firstname], [lastname], [idperson], [email], [age])
        VALUES (?, ?, ?, ?, ?);
    """

    params = [
        student.firstname
        , student.lastname
        , student.idperson
        , student.email
        , student.age
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json( sqlscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[firstname]
            ,[lastname]
            ,[idperson]
            ,[email]
            ,[age]
        FROM [academics].[students]
        WHERE email = ?;
    """

    params = [student.email]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


## CAREERS INTERACTION FUNCTIONS ##

async def add_career(student_id: int, career_id: int) -> StudentCareer:

    insert_script = """
        INSERT INTO [academics].[student_careers] ([student_id], [career_id], [enrollment_date], [active])
        VALUES (?, ?, ?, ?);
    """

    params = [
        student_id,
        career_id,
        datetime.now(),
        True
    ]

    try:
        await execute_query_json(insert_script, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
            sc.career_id
            , c.name as career_name
            , c.school_id
            , s.name as school_name
            , sc.enrollment_date
            , sc.active
        FROM academics.student_careers sc
        inner join academics.careers c 
        on sc.career_id = c.id
        INNER JOIN academics.schools s
        on c.school_id = s.id
        WHERE sc.student_id = ?
        and sc.career_id = ?;
    """

    params = [student_id, career_id]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

async def get_all_careers(student_id: int) -> list[StudentCareer]:
    select_script = """
        SELECT
            sc.career_id
            , c.name as career_name
            , c.school_id
            , s.name as school_name
            , sc.enrollment_date
            , sc.active
        FROM academics.student_careers sc
        inner join academics.careers c
        on sc.career_id = c.id
        INNER JOIN academics.schools s
        on c.school_id = s.id
        WHERE sc.student_id = ?
    """

    params = [student_id]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No careers found for the student")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")


async def get_one_career(student_id: int, career_id: int) -> StudentCareer:
    select_script = """
        SELECT
            sc.career_id
            , c.name as career_name
            , c.school_id
            , s.name as school_name
            , sc.enrollment_date
            , sc.active
        FROM academics.student_careers sc
        inner join academics.careers c 
        on sc.career_id = c.id
        INNER JOIN academics.schools s
        on c.school_id = s.id
        WHERE sc.student_id = ?
        and sc.career_id = ?;
    """

    params = [student_id, career_id]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No careers found for the student")

        return dict_result[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")


async def remove_career(student_id: int, career_id: int) -> str:
    delete_script = """
        DELETE FROM [academics].[student_careers]
        WHERE [student_id] = ? AND [career_id] = ?;
    """

    params = [student_id, career_id]

    try:
        await execute_query_json(delete_script, params=params, needs_commit=True)
        return "CAREER REMOVED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def update_career_info(career_data: StudentCareer) -> StudentCareer:
    dict = career_data.model_dump(exclude_none=True)
    keys = [ k for k in  dict.keys() ]
    keys.remove('student_id')
    keys.remove('career_id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [academics].[student_careers]
        SET {variables}
        WHERE [student_id] = ? AND [career_id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( career_data.student_id )
    params.append( career_data.career_id )

    try:
        await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
            sc.career_id
            , c.name as career_name
            , c.school_id
            , s.name as school_name
            , sc.enrollment_date
            , sc.active
        FROM academics.student_careers sc
        inner join academics.careers c 
        on sc.career_id = c.id
        INNER JOIN academics.schools s
        on c.school_id = s.id
        WHERE sc.student_id = ?
        and sc.career_id = ?;
    """

    params = [career_data.student_id, career_data.career_id]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")