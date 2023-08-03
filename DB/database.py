import json
from collections import defaultdict

import psycopg2

from DB import query

Query = query.Query
class Req:

    @staticmethod
    def req_schedule(group: str, week: str):
        group, week = str(group), str(week)

        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)  #TODO: Перенести данные в отдельный файл

        with conn.cursor() as cursor:
            cursor.execute(Query.schedule_get(group, week))

            fetchall = cursor.fetchall()
            json_data = {
                "group": fetchall[0][0],
                "week": fetchall[0][1],
                "schedule": defaultdict(list)
            }

            for row in fetchall:
                day = row[2].replace('(', '').replace(')', '').split(',')
                subject = row[6]
                room = row[8]
                teacher = row[7]

                json_data['schedule'][day[1]].append({
                    "indexDay": day[0],
                    "lesson": subject,
                    "classroom": room,
                    "teachers": teacher
                })

        conn.close()
        # Convert JSON data to a formatted string and return
        return json.dumps(json_data, indent=4, ensure_ascii=False) #Собираем json

    @staticmethod
    def req_news():
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)  # TODO: Перенести данные в отдельный файл
        data = {}
        with conn.cursor() as cursor:
            cursor.execute(Query.news_get())
            fetchall = cursor.fetchall()
            print(fetchall)
            for row in fetchall:
                article_id = int(row[0])
                title = str(row[1])
                #text = str(row[2])
                #views = row[3]
                #image = row[4] if row else None
                data[0]['title'] = title
                #data[article_id]['description'] = text
                #data[article_id]['image'] = image
                #data[article_id]['views'] = views

        conn.close()
        json_data = json.dumps(data)
        # Convert JSON data to a formatted string and return
        return json.dumps(json_data, indent=4, ensure_ascii=False)  # Собираем json