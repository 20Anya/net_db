import psycopg2

def create_table_client(conn):
    with conn.cursor() as cur:
        cur.execute('''
    CREATE TABLE IF NOT EXISTS client(
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    surname VARCHAR(40) NOT NULL,
    email VARCHAR(60) NOT NULL
    );
    ''')
        cur.execute(""" 
    CREATE TABLE IF NOT EXISTS phone_numbers(
    id SERIAL primary key,
    number integer,
    client_id integer not null references client(client_id) on delete cascade
    );
    """)
    conn.commit()

def add_new_client(conn, name, surname, email):
    with conn.cursor() as cur:
        cur.execute('''
    INSERT INTO client(name, surname, email)
    VALUES (%s, %s, %s);
    ''', (name, surname, email))
    conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
    INSERT INTO phone_numbers(number, client_id)
    VALUES (%s, %s);
    ''', (phone, client_id))
    conn.commit()

def update_client(conn, client_id, name=None, surname=None, email=None):
    with conn.cursor() as cur:
        if name is not None:
            cur.execute("""update client set name = %s 
                                       where client_id = %s;
                                    """, (name, client_id))
        if surname is not None:
            cur.execute("""update client set surname = %s 
                                       where client_id = %s;
                                    """, (surname, client_id))
        if email is not None:
            cur.execute("""update client set email = %s 
                                       where client_id = %s;
                                    """, (email, client_id))
    conn.commit()

def update_phone(conn, client_id, old_phone, new_phone):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE phone_numbers
        SET number = %s
        WHERE client_id = %s and number = %s;
        ''', (new_phone, client_id, old_phone))
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
    UPDATE phone_numbers
    SET number = REPLACE(number, %s, '')
    WHERE client_id = %s;
    ''', (phone, client_id))
    conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM client
        WHERE client_id = %s
        ''', (client_id,))
    conn.commit()

def find_client(conn, name=None, surname=None, email=None):
    with conn.cursor() as cur:
        cur.execute('''
    SELECT client_id FROM client
    WHERE name=%s and surname = %s or email = %s;
    ''', (name,surname, email))
        print(cur.fetchall()[0][0])

def find_client_with_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT client_id FROM phone_numbers
        WHERE number = %s;
        ''', (phone,))
        print(cur.fetchall()[0][0])


if __name__ == "__main__":
    database =                   #  Введите название базы данных
    user =                       #  Введите имя пользователя
    password =                   #  Введите пароль

    with psycopg2.connect(database=database, user=user, password=password) as conn:
        create_table_client(conn)
        add_new_client(conn, "Лиза", "Иванова", "...@mail.com")
        add_new_client(conn, "Маша", "Сергеевна", "1...@mail.com")
        add_new_client(conn, "Маша", "Иванова", "2...@mail.com")
        add_phone(conn, 1, 123)
        add_phone(conn, 2, 234)
        add_phone(conn, 3, 345)
        find_client(conn, "Лиза", "Иванова")
        find_client_with_phone(conn, 345)
        add_phone(conn, 1, 893706375)
        delete_client(conn, 2)
        add_phone(conn, 3, 893706375)
        update_phone(conn, 1, 123, 666)
        find_client_with_phone(conn, 666)
        update_client(conn, 1, 'Сергей', 'Иванов')
    
    conn.close()












