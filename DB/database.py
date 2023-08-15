import json
from collections import defaultdict
import psycopg2
import datetime
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
        return json_data

    @staticmethod
    def req_news():
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)  # TODO: Перенести данные в отдельный файл
        data = []
        with conn.cursor() as cursor:
            cursor.execute(Query.news_get())
            fetchall = cursor.fetchall()
            for row in fetchall:
                dict_row = {}
                print(int(row[0]))
                postId = int(row[0])
                title = str(row[1])
                text = str(row[2])
                views = row[3]
                image_url = row[4] if row else None
                posted_at = row[5]
                posted_for = row[6]
                dict_row['postId'] = postId
                dict_row['title'] = title
                dict_row['description'] = text
                dict_row['image_url'] = image_url
                dict_row['views'] = views
                dict_row['posted_at'] = posted_at
                dict_row['posted_for'] = posted_for
                data.append(dict_row)
        conn.close()
        json_data = str(data)
        # Convert JSON data to a formatted string and return
        return json_data

    @staticmethod
    def req_groups():
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)  # TODO: Перенести данные в отдельный файл
        data = []
        with conn.cursor() as cursor:
            cursor.execute(Query.groups_get())
            fetchall = cursor.fetchall()
            for row in fetchall:
                data.append(row[0])
        conn.close()
        json_data = str(data)
        # Convert JSON data to a formatted string and return
        return json_data


class Post:
    @staticmethod
    def post_news(Article):
        dt = datetime.datetime.now()
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)
        posted_for = datetime.datetime.strptime(Article.posted_for, '%Y-%m-%d %H:%M:%S')
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO news (title, text, image, posted_at, posted_for) VALUES (%s, %s, %s, %s, %s)",
                (Article.title, Article.text, Article.image, dt, posted_for)) #TODO: Перенос в query
        conn.commit()
        conn.close()