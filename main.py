from fastapi import FastAPI, Response, Request, Header
from DB import database
from Cloud import notifications
from news import Article

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
async def create_news_article(article: Article):
    database.Post.post_news(article)
    return 200

@app.get("/schedule/{group}/{week}")
def get_schedule(group: str, week: int):
    week_type = "Числитель" if week == 0 else "Знаменатель"
    schedule = database.Req.req_schedule(group, week_type)
    return schedule

@app.get("/schedule/notify")
def notification_schedule_update():
    notifications.notify_schedule()
    return 200

@app.get("/news/notify")
def notification_news_update():
    notifications.notify_news()
    return 200