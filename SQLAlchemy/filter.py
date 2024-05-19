import pymysql
import re
from pymysql.converters import escape_string

filter_table = {
    "single_quote": r"'",
    "semicolon": r";",
    "comment1": r"--",
    "comment2": r"/\*.*\*/",
    "union": r"UNION",
    "or_operator": r"OR",
    "and_operator": r"AND",
    "delete": r"DELETE",
    "drop": r"DROP",
    "percent": r"%"
}


def filter_input(input_str):
    for key, pattern in filter_table.items():
        if re.search(pattern, input_str, re.IGNORECASE):
            raise ValueError(f"Invalid input: {key} detected in input.")
    return input_str

def insert_data(username, password):
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            passwd="123456",
            database="students"
        )
        cursor = conn.cursor()
        clean_name = filter_input(username)
        clean_password = filter_input(password)
        sql = f"INSERT INTO students (name, password) VALUES ('{escape_string(clean_name)}', '{escape_string(clean_password)}')"
        cursor.execute(sql)
        conn.commit()
        print("Data inserted successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()


name1 = "John' OR '1'=1"
password1 = "mypassword!@#123"
print(f"input example 1: username = {name1}, password = {password1}")
insert_data(name1, password1)

name2 = "John"
password2 = "john123456"
print(f"input example 2: username = {name2}, password = {password2}")
insert_data(name2, password2)
