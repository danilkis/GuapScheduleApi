
from fastapi import FastAPI, Response, Request
import json
from DB import database
from Cloud import notifications
app = FastAPI()

@app.get("/news")
async def get_news():
    news = database.Req.req_news()
    return news

@app.post("/news/add")
async def post_news(request: Request):
    data = await request.json()
    with open("example.txt", "a") as f:
        f.write(data["title"] + "\n")
        f.write(data["text"] + "\n")
        f.write(data["date"] + "\n")
    return {"message": "Article appended successfully"}

@app.get("/schedule/{group}/{week}")
def get_schedule(group: str, week: int):
    week_type = "Числитель" if week == 0 else "Знаменатель"
    schedule = database.Req.req_schedule(group, week_type)
    return schedule

@app.get("/schedule/notify")
def notification_schedule_update():
    notifications.notify_schedule()
    return {"message": "SENT"}

@app.get("/news/notify")
def notification_news_update():
    notifications.notify_news()
    return {"message": "SENT"}