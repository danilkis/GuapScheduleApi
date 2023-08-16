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

        @staticmethod
        def groups_get() -> str:
                return (
                        "SELECT group_number FROM groups")

        @staticmethod
        def changes_get() -> str:
            return (
                "SELECT g.group_number, wt.week_name, wd.week_name AS week_days_info, t.pair_number, t.start_time, t.end_time, l.lesson_name, tr.name AS teacher_name, cl.classroom_name\n"
                "FROM changes c\n"
                "JOIN groups g ON g.id = c.group_id\n"
                "JOIN week_type wt ON wt.id = c.week_type_id\n"
                "JOIN week_days wd ON wd.week_number = c.week_days_id\n"
                "JOIN lesson l ON l.lesson_number = c.lesson_number_id\n"
                "JOIN time t ON t.pair_number = c.pair_number_id\n"
                "JOIN teachers tr ON tr.teacher_number = c.teacher_number_id\n"
                "JOIN classroom cl ON cl.classroom_number = c.classroom_number_id;")