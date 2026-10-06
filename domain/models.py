# domain/models.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Person:
    name: str
    document: str
    signature_url: Optional[str] = None

@dataclass
class Course:
    name: str
    duration_hours: int
    start_date: date
    end_date: date

@dataclass
class CourseCompletion:
    tenant_id: str
    student: Person
    instructor: Person
    course: Course