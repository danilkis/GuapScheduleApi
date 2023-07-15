
from fastapi import FastAPI, Response, Request
import json

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

college_schedule = {
    "001": {
        "Monday": [
            {
                "subject": "Math",
                "room": "101",
                "teachers": ["John Doe", "Jane Smith"]
            },
            {
                "subject": "Physics",
                "room": "201",
                "teachers": ["John Doe"]
            }
        ],
        "Tuesday": [
            {
                "subject": "Chemistry",
                "room": "301",
                "teachers": ["Jane Smith"]
            }
        ],
        # ... and so on for other days
    },
    "002": {
        # schedule for group2
    },
    # ... and so on for other groups
}


@app.get("/schedule/{group}/{week}")
def get_schedule(group: str, week: int):
    if group not in college_schedule:
        return {"error": f"Group '{group}' not found."}

    if week not in [0, 1]:
        return {"error": "Week should be either 0 or 1."}

    schedule = college_schedule[group]
    week_type = "even" if week == 0 else "odd"

    response = {}
    for day, subjects in schedule.items():
        response[day] = []
        for subject in subjects:
            response[day].append({
                "subject": subject["subject"],
                "room": subject["room"],
                "teachers": subject["teachers"]
            })

    return {
        "group": group,
        "week": week_type,
        "schedule": response
    }