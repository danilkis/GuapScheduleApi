from pydantic import BaseModel
class Changes(BaseModel):
    group: str
    week: str
    weekday: str
    lessonNum: str
    lesson: str
    classroom: str
    teacher: str
    indexDay: str
    for_date: str

