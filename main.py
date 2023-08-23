from typing import List

import uvicorn
from fastapi import FastAPI, Response, Request, Header
from DB import database
from Cloud import notifications
from Models.changes import Changes
from Models.news import Article

app = FastAPI()

@app.get("/news")
async def get_news():
    news = database.Req.req_news()
    return news

@app.get("/group")
async def get_groups():
    groups = database.Req.req_groups()
    return groups

@app.post("/news/add")
async def post_news(article: Article):
    database.Post.post_news(article)
    return 200

@app.get("/schedule/{group}/{week}")
async def get_schedule(group: str, week: int):
    week_type = "Числитель" if week == 0 else "Знаменатель"
    schedule = database.Req.req_schedule(group, week_type)
    return schedule

@app.get("/schedule/changes")
def get_schedule_changes():
    changes = database.Req.req_changes()
    return changes

@app.post("/schedule/add/changes")
def parse_lessons(lessons: List[Changes]):
    for changes in lessons:
        database.Post.post_schedule_change(changes)
    return 200

@app.get("/schedule/notify")
async def notification_schedule_update():
    notifications.notify_schedule()
    return 200

@app.get("/news/notify")
async def notification_news_update():
    notifications.notify_news()
    return 200