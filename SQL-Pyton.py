import psycopg2


def create_db(cur):
    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        surname VARCHAR(40) NOT NULL,
        email TEXT NOT NULL);
        """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id_phone SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES clients(id),
        phone VARCHAR(30) UNIQUE);
        """)
    
def add_clients(cur, name, surname, email):
    cur.execute("""
    INSERT INTO clients(name, surname, email) VALUES (%s, %s, %s);
    """, (name, surname, email))
   
def add_phones(cur, client_id, phone):
    cur.execute("""
    INSERT INTO phones(client_id, phone) VALUES(%s, %s);
    """,(client_id, phone))
                    
def change_client_info(cur):
    print('Чтобы изменить данные о клиенте введите следующие команды: \n'
            '1 - изменить имя \n'
            '2 - изменить фамилию \n'
            '3 - изменить e-mail \n'
            '4 - изменить номер телефона \n'
            '0 - выход из программы')
    while True:
        command = int(input('Введите номера команды для изменения данных о клиенте: '))
        if command == 1:
            id_name = input('Для того, чтобы изменить имя клиента, введите его id: ')
            change_name = input('Введите новое имя: ')
            cur.execute("""
            UPDATE clients SET name=%s WHERE id=%s;
            """,(change_name, id_name))
                        
        elif command == 2:
            id_surname = input('Для того, чтобы изменить фамилию клиента, введите его id: ')
            change_surname = input('Введите новую фамилию: ')
            cur.execute("""
            UPDATE clients SET surname=%s WHERE id=%s;
            """,(change_surname, id_surname))
                        
        elif command == 3:
            id_email = input('Для того, чтобы поменять e-mail клиента, введите его id: ')
            change_email = input('Введите новый e-mail: ')
            cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s;
            """,(change_email, id_email))
                        
        elif command == 4:
            old_phone = input('Введите номер телефона, который хотите заменить: ')
            new_phone = input('Введите новый номер телефона: ')
            cur.execute("""
            UPDATE phones SET phone=%s WHERE phone=%s,
            """,(new_phone, old_phone))
                        
        elif command == 0:
            break
            
        else:
            print('Проверьте правильность ввода команды') 


def delete_phones(conn):
    id_client = input('Ввдеите id клиента, номер которого вы хотите удалить: ')
    phone_delete = input('Введите номер, который хотите удалить: ')
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones WHERE client_id=%s AND phone=%s
        """, (phone_delete, id_client))

def delete_clients(conn):
    id_client = input('Для удаления клиента введите его id: ')
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones WHERE id_client=%s
        """, (id_client,))
        cur.execute("""
        DELETE FROM clients WHERE id_client=%s
        """, (id_client,))
        
def find_clients(cur):
    print('Для запроса информации о клиенте выберите параметр поиска: \n'
          '1 - поиск по имени \n'
          '2 - поиск по фамилии \n'
          '3 - поиск по e-mail \n'
          '4 - поиск по номеру телефона \n'
          '0 - выход из программы')
    while True:
        command = int(input('Введеите номер команды для поиска информации о клиенте: '))
        if command == 1:
            search_name = input('Введите имя клиента: ')
            cur.execute("""
            SELECT id, name, surname, email, phone FROM clients cl
            LEFT JOIN phones ph on cl.id = ph.client_id
            WHERE name=%s
            """, (search_name,))
            print(cur.fetchall())
            
        elif command == 2:
            search_surname = input('Введите фамилию клиента: ')
            cur.execute("""
            SELECT id, name, surname, email, phone FROM clients cl
            JOIN phones ph on cl.id = ph.client_id
            WHERE surname=%s
            """, (search_surname,))
            print(cur.fetchall())
        
        elif command == 3:
            search_email = input('Введите e-mail клиента: ')
            cur.execute("""
            SELECT id, name, surname, email, phone FROM clients cl
            JOIN phones ph on cl.id = ph.client_id
            WHERE email=%s
            """, (search_email,))
            print(cur.fetchall())
            
        elif command == 4:
            search_phone = input('Введите номер телефона клиента: ')
            cur.execute("""
            SELECT id, name, surname, email, phone FROM clients cl
            JOIN phones ph on cl.id = ph.client_id
            WHERE phone=%s
            """, (search_phone,))
            print(cur.fetchall())
        
        elif command == 0:
            break
        
        else:
            print('Проверьте правильность ввода команды')
            
with psycopg2.connect(host='localhost', database='clients_db', user='postgres', password='Starscream1988', port='5432') as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)
        create_db(cur)
        add_clients(cur, 'Boba', 'Fett', 'fett@gmail.com')
        add_clients(cur, 'Tony', 'Stark', 'stark@gmail.com')
        add_clients(cur, 'Anakin', 'Skywalker', 'darkside@ofpower.com')
        add_clients(cur, 'Natasha', 'Romanoff', 'romoff@inbox.ru')
        add_phones(cur, 1, '+7656145500')
        add_phones(cur, 2, '+1556633999')
        add_phones(cur, 3, '+6666666666')
        add_phones(cur, 4, '+74732023333')
        change_client_info(cur)
        delete_clients(conn)
        delete_phones(conn)
        find_clients(cur)
conn.close

    
            
        
               
    
                

    
            