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
                pair_number = row[3]
                room = row[8]
                teacher = row[7]

                json_data['schedule'][day[1]].append({
                    "indexDay": day[0],
                    "lessonNum": pair_number,
                    "lesson": subject,
                    "classroom": room,
                    "teachers": teacher
                })

        conn.close()
        # Convert JSON data to a formatted string and return
        return json_data

    @staticmethod
    def req_changes():
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)  #TODO: Перенести данные в отдельный файл

        json_data = []

        with conn.cursor() as cursor:
            cursor.execute(Query.changes_get())

            fetchall = cursor.fetchall()

            for row in fetchall:
                dict_row = {}
                dict_row['group'] = row[0]
                dict_row['week'] = row[1]
                day = row[2].replace('(', '').replace(')', '').split(',')
                dict_row['lessonNum'] = row[3]
                dict_row['lesson'] = row[6]
                dict_row['classroom'] = row[8]
                dict_row['teacher'] = row[7]
                dict_row['indexDay'] = day[0]
                json_data.append(dict_row)
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
                dict_row['postId'] = int(row[0])
                dict_row['title'] = str(row[1])
                dict_row['description'] = str(row[2])
                dict_row['views'] = row[3]
                dict_row['image_url'] = row[4] if row else None
                dict_row['posted_at'] = row[5]
                dict_row['posted_for'] = row[6]
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


    @staticmethod
    def post_schedule_change(data):
        # Parse the incoming JSON data
        group = data.get("group")
        week = data.get("week")
        day = data.get("day")
        index_day = data.get("indexDay")
        lesson = data.get("lesson")
        classroom = data.get("classroom")
        teachers = data.get("teachers")

        conn = psycopg2.connect(
            dbname='guap_app',
            user='guap',
            password='FSPO',
            host='pavlovskhomev3.duckdns.org',
            port=5432)

        with conn.cursor() as cursor:
            # Here you would execute appropriate SQL queries to update the schedule
            # based on the provided data. You would need to determine the proper schema
            # and fields in your database to perform the update.

            # For example:
            update_query = (
                "UPDATE schedule "
                "SET lesson_name = %s, classroom_name = %s, teacher_name = %s "
                "WHERE group_id = %s AND week_name = %s AND week_day = %s AND index_day = %s"
            )
            cursor.execute(update_query, (lesson, classroom, teachers, group, week, day, index_day))

            conn.commit()

        conn.close()

        return {"message": "Schedule change successful"}