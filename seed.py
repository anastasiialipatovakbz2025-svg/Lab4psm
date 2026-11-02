
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
        ) as connection:

            with connection.cursor() as cursor:

                # Додаємо будинки, якщо таблиця порожня
                cursor.execute("SELECT COUNT(*) FROM buildings")
                if cursor.fetchone()[0] == 0:
                    buildings = [
                        ("вул. Шевченка, 10", "Львів", 5),
                        ("вул. Франка, 15", "Львів", 9),
                        ("вул. Городоцька, 25", "Львів", 7),
                        ("вул. Зелена, 30", "Львів", 10),
                        ("вул. Наукова, 12", "Львів", 12),
                        ("вул. Личаківська, 45", "Львів", 6),
                        ("вул. Коперника, 8", "Львів", 4),
                        ("вул. Стрийська, 20", "Львів", 8),
                        ("вул. Сахарова, 17", "Львів", 9),
                        ("вул. Кульпарківська, 33", "Львів", 11),
                    ]

                    cursor.executemany(
                        """
                        INSERT INTO buildings (address, city, floors)
                        VALUES (%s, %s, %s)
                        """,
                        buildings
                    )

                # Додаємо власників, якщо таблиця порожня
                cursor.execute("SELECT COUNT(*) FROM owners")
                if cursor.fetchone()[0] == 0:
                    owners = [
                        (f"Власник {i}", f"+380501000{i:04d}",
                         f"owner{i}@example.com")
                        for i in range(1, 16)
                    ]

                    cursor.executemany(
                        """
                        INSERT INTO owners (full_name, phone, email)
                        VALUES (%s, %s, %s)
                        """,
                        owners
                    )

                # Отримуємо ID будинків та власників
                cursor.execute("SELECT id FROM buildings ORDER BY id")
                building_ids = [row[0] for row in cursor.fetchall()]

                cursor.execute("SELECT id FROM owners ORDER BY id")
                owner_ids = [row[0] for row in cursor.fetchall()]

                # Додаємо 50 квартир, якщо таблиця порожня
                cursor.execute("SELECT COUNT(*) FROM apartments")

                if cursor.fetchone()[0] == 0:
                    apartments = []

                    for i in range(50):
                        apartments.append((
                            i + 1,
                            i % 3 + 1,
                            35 + i % 6 * 10,
                            50000 + i * 2500,
                            building_ids[i % len(building_ids)],
                            owner_ids[i % len(owner_ids)]
                        ))

                    cursor.executemany(
                        """
                        INSERT INTO apartments (
                            apartment_number,
                            rooms,
                            area,
                            price,
                            building_id,
                            owner_id
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        apartments
                    )

                # Перевіряємо кількість записів
                for table in ("buildings", "owners", "apartments"):
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table}"
                    )
                    print(f"{table}: {cursor.fetchone()[0]} записів")

                print("Ініціалізація бази даних завершена!")

    except psycopg.Error as error:
        print("Помилка роботи з PostgreSQL:")
        print(error)


if __name__ == "__main__":
    main()
