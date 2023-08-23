import json
from collections import defaultdict
import psycopg2
import datetime
from DB import query
from Models.news import Article
from Models.changes import Changes
Query = query.Query
class Req:

    @staticmethod
    def req_schedule(group: str, week: str):
        group, week = str(group), str(week)

        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='daniel',
            password='XMBu8:EPxRSj\F',
            host='database.leftbrained.space',
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
            user='daniel',
            password='XMBu8:EPxRSj\F',
            host='database.leftbrained.space',
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
        MONTH_NAMES = {
            "January": "января",
            "February": "февраля",
            "March": "марта",
            "April": "апреля",
            "May": "мая",
            "June": "июня",
            "July": "июля",
            "August": "августа",
            "September": "сентября",
            "October": "октября",
            "November": "ноября",
            "December": "декабря",
        }
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='daniel',
            password='XMBu8:EPxRSj\F',
            host='database.leftbrained.space',
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
                posted_for_datetime = row[6]
                month = posted_for_datetime.strftime('%B')
                formatted_month = MONTH_NAMES.get(month, month)
                formatted_posted_for = posted_for_datetime.strftime(f'%-d {formatted_month} %Y года, %H:%M')
                dict_row['posted_for'] = formatted_posted_for
                data.append(dict_row)
        conn.close()
        json_data = data
        # Convert JSON data to a formatted string and return
        return json_data

    @staticmethod
    def req_groups():
        conn = psycopg2.connect(  ##Подключение к БД
            dbname='guap_app',
            user='daniel',
            password='XMBu8:EPxRSj\F',
            host='database.leftbrained.space',
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
            user='daniel',
            password='XMBu8:EPxRSj\F',
            host='database.leftbrained.space',
            port=5432)
        posted_for = datetime.datetime.strptime(Article.posted_for, '%Y-%m-%d %H:%M:%S')
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO news (title, text, image, posted_at, posted_for) VALUES (%s, %s, %s, %s, %s)",
                (Article.title, Article.text, Article.image, dt, posted_for)) #TODO: Перенос в query
        conn.commit()
        conn.close()


    @staticmethod
    def post_schedule_change(Changes):
        conn = psycopg2.connect(
            dbname='guap_app',
            user='daniel',
            password='XMBu8:EPxRSj\F',
            host='database.leftbrained.space',
            port=5432)

        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO changes (created_at, for_date, group_id, week_type_id, week_days_id, pair_number_id, lesson_number_id, teacher_number_id, classroom_number_id)\n"
                           "SELECT\n"
                           "NOW(),\n"
                           "%s,\n"
                            "g.id AS group_id,\n"
                            "wt.id AS week_type_id,\n"
                            "wd.week_number AS week_days_id,\n"
                            "t.pair_number AS pair_number_id,\n"
                            "l.lesson_number AS lesson_number_id,\n"
                            "tr1.teacher_number AS teacher_number_id,\n"
                            "cl1.classroom_number AS classroom_number_id\n"
                            "FROM groups g\n"
                            "JOIN schedule s ON g.id = s.group_id\n"
                            "JOIN week_type wt ON wt.id = s.week_type_id\n"
                            "JOIN week_days wd ON wd.week_number = s.week_days_id\n"
                            "JOIN lesson l ON l.lesson_name = %s\n"
                            "JOIN time t ON t.pair_number = s.pair_number_id\n"
                            "JOIN teachers tr ON tr.teacher_number = s.teacher_number_id\n"
                            "JOIN teachers tr1 ON tr1.name = %s\n"
                            "JOIN classroom cl ON cl.classroom_number = s.classroom_number_id\n"
                            "JOIN classroom cl1 ON cl1.classroom_name = %s"
                            "WHERE g.group_number = %s\n"
                            "AND wt.week_name = %s\n"
                            "AND wd.week_name = %s"
                            "AND s.pair_number_id = %s;",
                (Changes.for_date, Changes.lesson, Changes.teacher, Changes.classroom, Changes.group, Changes.week, Changes.weekday, Changes.lessonNum))

            conn.commit()

        conn.close()

        return {"message": "Schedule change successful"}