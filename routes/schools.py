from fastapi import APIRouter, status

from models.schools import Schools


from controllers.schools import (
   get_all_schools
)

router = APIRouter(prefix="/schools")

@router.get("/", tags=["Schools"], status_code=status.HTTP_200_OK)
async def read_schools():
    return await get_all_schools()
