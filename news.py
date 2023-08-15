from pydantic import BaseModel
class Article(BaseModel):
    title: str
    text: str
    image: str
    posted_for: str