from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Student(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el estudiante"
    )

    firstname: Optional[str] = Field(
        description="Primer nombre del estudiante",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Juan","Maria"]
    )

    lastname: Optional[str] = Field(
        description="Primer nombre del estudiante",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Perez","Martinez"]
    )

    idperson: Optional[str] = Field(
        pattern=r"^[A-Za-z0-9' -]+$"
    )

    email: Optional[str] = Field(
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["usuario@example.com"]
    )

    age: Optional[int] = Field(
        ge=14
    )