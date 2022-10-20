import sqlite3 as sqlt

db_name = 'user_database.db'


def start_db():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS "data" ("id"	INTEGER,'
                 '"tg_id"	INTEGER,'
                 '"first_name"	BLOB,'
                 '"last_name"	BLOB,'
                 '"username"	BLOB,'
                 'PRIMARY KEY("id" AUTOINCREMENT));')
    base.commit()


def db_add(id, first_name, last_name, username):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    usrnm = '@' + username
    cur.execute('INSERT INTO data VALUES (null, ?, ?, ?, ?)', (id, first_name, last_name, usrnm,))
    base.commit()
    base.close()


def get_tg_id():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    users = cur.execute('SELECT tg_id from data').fetchall()
    base.close()
    user_list = list()
    for i in users:
        user_list.append(i[0])
    return user_list


def all_user():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    users = cur.execute('SELECT tg_id from data').fetchall()
    base.close()
    return users


def create_post_db():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS "post_data" '
                 '("chat_id"	INTEGER,'
                 '"message_id" INTEGER );')
    base.commit()


def db_post(chat_id, message_id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    print(f'*** {chat_id}  ***{message_id}')
    cur.execute('DELETE from post_data ')
    cur.execute('INSERT INTO post_data VALUES (?, ?)', (chat_id, message_id,))
    base.commit()
    base.close()


def post_data():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    pst = cur.execute('SELECT * from post_data').fetchall()
    base.close()
    return pst