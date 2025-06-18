import psycopg2


def add_users():

    connection = psycopg2.connect(
        host="localhost",
        port=5433,
        user="postgres",
        password="postgres",
        database="social_network_db"
    )
    with connection.cursor() as cursor:
        with open("users_1m.csv", 'r', encoding='utf-8', errors='replace') as file:
            next(file)
            cursor.copy_expert("COPY users(first_name, last_name, birth_date, gender, interests, city, hashed_password) FROM STDIN WITH CSV", file)

        connection.commit()
    connection.close()

if __name__ == "__main__":
    add_users()