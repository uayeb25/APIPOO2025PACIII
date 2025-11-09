import json
import logging

from fastapi import HTTPException

from models.students import Student
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



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





