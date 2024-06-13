import psycopg2
from psycopg2 import OperationalError

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="my_database",
                user="postgres",
                host="localhost",
                password="qwerty",
                port="5432"
            )
            print("Подключение к базе данных успешно!")
        except OperationalError as err:
            print("Подключение к базе данных не удалось:", err)
            self.conn = None

    def add_user(self, name, email, hpsw):
        try:
            self.__cur = self.conn.cursor()
            self.__cur.execute(f"SELECT COUNT(*) FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                return False

            self.__cur.execute("INSERT INTO users(name, email, psw) VALUES(%s, %s, %s)", (name, email, hpsw))
            self.conn.commit()
            self.__cur.close()
        except Exception as err:
            print(f"Ошибка при добавлении пользователя в  БД: {err}")
            return False
        return False

    def getUser(self, user_id):
        try:
            self.__cursor = self.conn.cursor()
            self.__cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except Exception as err:
            print(f"Ошибка при получении данных из БД: {err}")

        return False
    
    def get_user_email(self, email):
        try:
            __cur = self.conn.cursor()
            __cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = __cur.fetchone()
            if not res:
                print('пользователь не найден')
                return False
            
            return res
        except Exception as err:
            print(err)
        return False
