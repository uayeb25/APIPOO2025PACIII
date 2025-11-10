from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Schools(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para la escuela"
    )

    name: Optional[str] = Field(
        description="Nombre de la escuela",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["Juan","Maria"]
    )

    code: Optional[str] = Field(
        description="Primer nombre del estudiante",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["Perez","Martinez"]
    )