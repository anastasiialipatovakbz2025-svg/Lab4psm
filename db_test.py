
import psycopg


def main():
    try:
        with psycopg.connect(
            host="localhost",
            port=5432,
            dbname="library",
            user="postgres",
            password="lab4psm_local_password",
            options="-c timezone=Europe/Kyiv"
        ) as connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    current_database(),
                    current_user,
                    current_setting('TimeZone');
            """)

            result = cursor.fetchone()

            print("Підключення до PostgreSQL успішне!")
            print("База даних:", result[0])
            print("Користувач:", result[1])
            print("Часовий пояс:", result[2])

    except psycopg.Error as error:
        print("Помилка підключення до PostgreSQL:")
        print(error)


if __name__ == "__main__":
    main()
