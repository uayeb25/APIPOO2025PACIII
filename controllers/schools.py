import json
import logging

from fastapi import HTTPException

from models.schools import Schools
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_all_schools() -> list[Schools]:

    selectscript = """
        SELECT [id]
            ,[name]
            ,[code]
        FROM [academics].[schools]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
