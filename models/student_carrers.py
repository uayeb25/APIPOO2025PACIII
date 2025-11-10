from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta
from typing import Optional
import re


class StudentCareer(BaseModel):
    student_id: Optional[int] = Field(
        description="El ID del estudiante",
        default=None
    )

    career_id: Optional[int] = Field(
        description="El ID de la carrera",
        default=None
    )

    career_name: Optional[str] = Field(
        description="Nombre de la carrera",
        default=None
    )

    school_id: Optional[int] = Field(
        description="El ID de la escuela a la que pertenece la carrera",
        default=None
    )

    school_name: Optional[str] = Field(
        description="Nombre de la escuela",
        default=None
    )

    enrollment_date: Optional[datetime] = Field(
        description="Fecha de inscripción del estudiante en la carrera",
        default=None
    )

    active: Optional[bool] = Field(
        description="Indica si el estudiante está activo en la carrera",
        default=True
    )