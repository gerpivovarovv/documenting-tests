import pymysql
import pymysql.cursors


class DB:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            database='lab_testing',
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    # Админ
    def get_user(self, login):
        self.cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
        return self.cursor.fetchone()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def add_user(self, login, nam, surname, patronymic, password, role):
        self.cursor.execute(
            "INSERT INTO users (login, nam, surname, patronymic, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
            (login, nam, surname, patronymic, password, role)
        )
        self.conn.commit()

    def update_user(self, user_id, login, nam, surname, patronymic, password, role):
        self.cursor.execute(
            """UPDATE users SET login=%s, name=%s, surname=%s, patronymic=%s, password=%s, role=%s
               WHERE user_id=%s""",
            (login, nam, surname, patronymic, password, role, user_id)
        )
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        self.conn.commit()

    # Инженер
    def get_all_test_objects(self):
        cursor = self.cursor
        cursor.execute("SELECT * FROM test_objects")
        return cursor.fetchall()

    def add_test_object(self, name, category, date, description):
        cursor = self.cursor
        cursor.execute("""
            INSERT INTO test_objects (name, category, received_date, description)
            VALUES (%s, %s, %s, %s)
        """, (name, category, date, description))
        self.conn.commit()

    def add_test_result(self, object_id, test_date, parameters, result):
        cursor = self.cursor
        cursor.execute("""
            INSERT INTO test_results (object_id, test_date, parameters, result)
            VALUES (%s, %s, %s, %s)
        """, (object_id, test_date, parameters, result))
        self.conn.commit()

    def get_results_for_expert(self, expert_id):
        self.cursor.execute("""
            SELECT tr.result_id, tobj.name AS object_name, tr.test_date, tr.parameters, tr.result
            FROM test_results tr
            JOIN test_objects tobj ON tr.object_id = tobj.object_id
            WHERE tr.expert_id = %s
            ORDER BY tr.test_date DESC
        """, (expert_id,))
        return self.cursor.fetchall()

    # Эксперт
    def get_protocol_by_result(self, result_id):
        self.cursor.execute("""
            SELECT * FROM protocols WHERE result_id = %s
        """, (result_id,))
        return self.cursor.fetchone()

    def save_protocol(self, result_id, summary):
        existing = self.get_protocol_by_result(result_id)
        if existing:
            self.cursor.execute("""
                UPDATE protocols SET summary = %s, generated_at = NOW() WHERE result_id = %s
            """, (summary, result_id))
        else:
            self.cursor.execute("""
                INSERT INTO protocols (result_id, summary) VALUES (%s, %s)
            """, (result_id, summary))
        self.conn.commit()
