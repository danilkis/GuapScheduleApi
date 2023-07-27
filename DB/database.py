import json
from collections import defaultdict
from DB import query
import psycopg2

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
            cursor.execute(Query.schedule(), (group, week,))

            fetchall = cursor.fetchall()
            print()

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

        # Convert JSON data to a formatted string and return
        return json.dumps(json_data, indent=4, ensure_ascii=False) #Собираем json