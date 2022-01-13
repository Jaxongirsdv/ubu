#import sqlite3
from datetime import datetime
#conn = sqlite3.connect("database.db", check_same_thread=False)
#cursor = conn.cursor()

import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="botxat"
)
cursor = conn.cursor(buffered=True)

print(conn)
# def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
# cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
# conn.commit()
def add_lang(user_id: int, lang: str):
    cursor.execute("INSERT INTO bot_users (user_id, lang) VALUES (%s, %s)", (user_id, lang))
    conn.commit()

def delete_lang(id:int):
    cursor.execute("DELETE FROM bot_users WHERE user_id="+str(id))
    conn.commit()

def add_contact_and_bot_id(id:int, num: str):
    cursor.execute("UPDATE bot_users SET numb='+"+ str(num) +"' WHERE user_id="+ str(id))
    cursor.execute("UPDATE employees SET bot_id="+ str(id) +" WHERE user_numb='+"+ str(num)+"'")
    conn.commit()


def get_final_nomer(orgname:str):
    print(orgname)
    cursor.execute("SELECT nomer FROM reg WHERE org='"+orgname+"' ORDER BY ID DESC LIMIT 1")
    conn.commit()
    row = cursor.fetchall()
    for no in row:
        n=no
    print(type(n[0]))
    return n[0]


def add_reg_and_get_nomer(bot_id:int,sendorg:str,sendfio:str,tema:str,org:str):

    #print(type(bot_id))
    #print(type(sendorg))
    #print(type(sendfio))
    #print(type(tema))
    #print(type(get_final_nomer()))
    nomer = str(int(get_final_nomer(org)) + 1)
    print(nomer)

    now = datetime.now()
    now= str(now.strftime("%d-%m-%Y %H:%M:%S"))
    # print(now)
    # print(type(now))
    for emp in select_employees_from_id(bot_id):
        fio=emp[1]
    executor= fio
    cursor.execute("INSERT INTO reg (send_to_org,send_to_fio,theme,bot_user_id,nomer,data,org,executor) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)",(sendorg,sendfio,tema,bot_id,nomer,now,org,executor))
    conn.commit()
    print(nomer)
    return nomer
def add_file_link(link:str,nomer:str):
    cursor.execute("UPDATE reg SET link='"+ str(link) +"' WHERE nomer="+ str(nomer))
    conn.commit()
def select_regs_by_bot_id(id:str):
    cursor.execute("SELECT * FROM reg WHERE bot_user_id='"+str(id)+"' ORDER BY ORG")
    conn.commit()
    row = cursor.fetchall()
    return row



def select_employees(user_numb: str):
    cursor.execute("SELECT * FROM employees WHERE user_numb='+" + str(user_numb) +"'")
    conn.commit()
    row = cursor.fetchall()
    return row
def select_employees_by_id(id: str):
    cursor.execute("SELECT * FROM employees WHERE bot_id=" + str(id))
    conn.commit()
    row = cursor.fetchall()
    return row
def select_employees_from_id(user_ids: int):
    cursor.execute("SELECT * FROM employees WHERE bot_id='" + str(user_ids) +"'")
    conn.commit()
    row = cursor.fetchall()
    # print(len(row))
    return row

def select_lang(user_id: int):
	cursor.execute("SELECT lang FROM bot_users WHERE user_id=" + str(user_id))
	conn.commit()
	rows = cursor.fetchall()
	return rows
