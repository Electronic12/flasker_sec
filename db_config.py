import psycopg2

try:
    connection = psycopg2.connect(
        host='localhost',
        user = "postgres",
        password = "postgres",
        database="name"
    )
# Table doredyar add.commitsiz
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")

# Databazada table doretmek ucin 
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users(
                id serial PRIMARY KEY,
                first_name varchar(50) NOT NULL,
                nick_name varchar(50) NOT NULL);"""
        )
        print("[INFO] Table created successfully")

# Databasa data goshmak postgrsql ucin 
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO users(first_name, nick_name) VALUES
            ('Mergen', 'Mergenow');"""
        )
        print("[INFO] Database created successfully")

# Databasa Request ugratmak
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT first_name FROM users WHERE nick_name = 'Mergenow';"""
        )
        print(cursor.fetchone())

# Databasa Request ugratmak
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """SELECT username FROM jora WHERE password = 'ke';"""
    #     )
    #     print(cursor.fetchone())

# Databasa Delete etmek ucin
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """DROP table users;"""
    #     )
    #     print("[INFO] Table was deleted")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] Connection closed")

