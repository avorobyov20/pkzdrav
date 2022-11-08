from django.conf import settings
import sqlite3


def update_sqlite_table(cmd):
    sqlite_connection = sqlite3.connect(settings.DATABASES['default']['NAME'])
    cursor = sqlite_connection.cursor()
    # print("Подключен к SQLite")
    cursor.execute(cmd)
    sqlite_connection.commit()
    print(cmd + " Запись успешно обновлена")
    cursor.close()
    sqlite_connection.close()
    # print("Соединение с SQLite закрыто")
