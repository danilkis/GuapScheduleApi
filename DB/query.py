import psycopg2


class Query:
        @staticmethod
        def schedule_get(group, week) -> str:
            return (
                    "SELECT groups.group_number, week_type.week_name, (week_days.week_number, week_days.week_name),\n"
                    "       time.pair_number, time.start_time, time.end_time, lesson.lesson_name, teachers.name, classroom.classroom_name\n"
                    "FROM groups\n"
                    "    JOIN schedule ON groups.id = schedule.group_id\n"
                    "    JOIN week_type ON week_type.id = schedule.week_type_id\n"
                    "    JOIN week_days ON week_days.week_number = schedule.week_days_id\n"
                    "    JOIN lesson ON lesson.lesson_number = schedule.lesson_number_id\n"
                    "    JOIN time ON time.pair_number = schedule.pair_number_id\n"
                    "    JOIN teachers ON teachers.teacher_number = schedule.teacher_number_id\n"
                    "    JOIN classroom ON classroom.classroom_number = schedule.classroom_number_id\n"
                    f"WHERE groups.group_number = '{group}' AND week_type.week_name = '{week}';")

        @staticmethod
        def news_get() -> str:
            return (
                "SELECT * FROM news")