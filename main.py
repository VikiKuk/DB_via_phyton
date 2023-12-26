import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute(""" DROP TABLE IF EXISTS phone;
                        DROP TABLE IF EXISTS client; 
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                surname VARCHAR(40),
                email VARCHAR(40) UNIQUE
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                phone_id SERIAL PRIMARY KEY,
                number VARCHAR(40) UNIQUE,
                client_id INTEGER REFERENCES client (client_id)
            );
            """)
        conn.commit()

def add_client(conn, p_name, surname, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(name, surname, email) VALUES (%s, %s, %s)
            """, (p_name, surname, email))
        conn.commit()

def add_phone_for_existing_client(conn, client_id, new_phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(number, client_id) VALUES (%s, %s) ON CONFLICT (number) DO NOTHING;
            """, (new_phone, client_id))
        conn.commit()

def update_client_info(conn, client_id, name=None, surname=None, email=None, old_phone=None, new_phone=None):
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE client SET  name = %s, surname = %s, email = %s WHERE client_id = %s
                """, (name, surname, email, client_id))
            cur.execute("""
               UPDATE phone SET  number = %s WHERE client_id = %s AND number = %s
               """, (new_phone, client_id, old_phone))
            conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
               DELETE FROM phone 
               WHERE client_id = %s AND number = %s;
               """, (client_id, phone))
        conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
               DELETE FROM client 
               WHERE client_id = %s;
               """, (client_id,))
        conn.commit()

def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if name != None or surname != None or email != None:
            cur.execute("""
                       SELECT * FROM client
                       WHERE (name = %s OR %s IS NULL)
                        AND (surname = %s OR %s IS NULL)
                        AND (email = %s OR %s IS NULL)
                       """, (name, name, surname, surname, email, email))
            print('Поиск по данным клиента')
            print(cur.fetchall())
        elif phone != None:
            cur.execute("""
                       SELECT cl.name, cl.surname, cl.email, ph.number FROM phone AS ph
                       JOIN client AS cl ON cl.client_id = ph.client_id
                       WHERE number = %s
                       """, (phone,))
            print('Поиск по телефону')
            print(cur.fetchall())
        else:
            print ('Заполните параметры для поиска')
        conn.commit()

        # Альтернатианя версия
        # if name != None or surname != None or email != None or phone != None:
        #     cur.execute("""
        #                SELECT cl.client_id, cl.name, cl.surname, cl.email, ph.number FROM client AS cl
        #                LEFT JOIN phone AS ph ON ph.client_id = cl.client_id
        #                WHERE (%s IS NULL AND (name = %s OR %s IS NULL)
        #                 AND (surname = %s OR %s IS NULL)
        #                 AND (email = %s OR %s IS NULL))
        #                 OR (number = %s AND %s IS NOT NULL)
        #                """, (phone, name, name, surname, surname, email, email, phone, phone))
        #     print(cur.fetchall())
        # else:
        #     print ('Заполните параметры для поиска')
        # conn.commit()



if __name__ == '__main__':
    with psycopg2.connect(database='client_db', user='postgres') as conn:
        python_id = create_db(conn)
        create_client = add_client(conn,'Иван', 'Тестовый', 'ivant@gamil.com')
        create_client2 = add_client(conn, 'Григорий', 'Петрович', 'gregory@gamil.com')
        create_client3 = add_client(conn, 'Вистория', 'Ручная', 'victoria@gamil.com')
        create_client4 = add_client(conn, 'Я_тебя', 'Буду_удалять', 'delete_client@gamil.com')
        create_client5 = add_client(conn, 'Иван', 'Петровский', 'ivanpetr@gamil.com')

        add_new_phone = add_phone_for_existing_client(conn, '1', '7903555')
        add_new_phone2 = add_phone_for_existing_client(conn, '2', '7912333')
        add_new_phone3 = add_phone_for_existing_client(conn, '2', '7900777')
        add_new_phone4 = add_phone_for_existing_client(conn, '3', '8899000')
        add_new_phone5 = add_phone_for_existing_client(conn, '3', '9999000')

        change_client_info = update_client_info(conn,  '3', 'Виктория', 'Рудная', 'victoria@gamil.com', '9999000', '1111111')
        delete_client_phone = delete_phone(conn,'2', '7900777')
        delete_clint_from_db = delete_client(conn, '4')


        find_client_db = find_client(conn, phone = '7903555')
        find_client_db = find_client(conn, surname='Тестовый')
        find_client_db = find_client(conn, name = 'Иван', surname='Петровский')
        find_client_db = find_client(conn, name='Иван')









