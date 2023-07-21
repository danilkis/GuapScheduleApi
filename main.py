
from fastapi import FastAPI, Response, Request
import json
from DB import database

app = FastAPI()

@app.get("/news")
async def read_file():
    with open("example.txt", "r") as f:
        lines = f.readlines()
        articles = []
        for i in range(0, len(lines), 3):
            title = lines[i].strip()
            text = lines[i+1].strip()
            date = lines[i+2].strip()
            article_dict = {"title": title, "text": text, "date": date}
            articles.append(article_dict)
        return Response(content=json.dumps(articles), media_type="application/json")

@app.post("/news")
async def append_file(request: Request):
    data = await request.json()
    with open("example.txt", "a") as f:
        f.write(data["title"] + "\n")
        f.write(data["text"] + "\n")
        f.write(data["date"] + "\n")
    return {"message": "Article appended successfully"}

@app.get("/schedule/{group}/{week}")
def get_schedule(group: str, week: int):
    week_type = "Числитель" if week == 0 else "Знаменатель"
    schedule = database.req_schedule(group, week_type)
    return schedule