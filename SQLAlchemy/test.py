from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.exc import IntegrityError

engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/students", echo=False)

metadata = MetaData()

students = Table(
    'students',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('password', String(50)),
    Column('mail', String(50), unique=True)
)

metadata.create_all(engine)

insert_queries = [
    text("INSERT INTO students (name, password, mail) VALUES (:name1, :password1, :mail1)").params(
        name1='Jack', password1="addfff", mail1="jack@qq.com"
    ),
    text("INSERT INTO students (name, password, mail) VALUES (:name2, :password2, :mail2)").params(
        name2='Jill', password2="addddd", mail2="jill@qq.com"
    ),
]

try:
    with engine.connect() as conn:
        for query in insert_queries:
            conn.execute(query)
        conn.commit()
except IntegrityError as e:
    error_message = str(e)
    if "Duplicate entry" in error_message:
        print("该邮箱已存在，请输入一个不同的邮箱。")
    else:
        print("发生完整性错误,", error_message)

select_query = text(
    "SELECT * FROM students WHERE mail LIKE :pattern").params(pattern='%qq.com%')

with engine.connect() as conn:
    result = conn.execute(select_query)
    columns = result.keys()
    for row in result:
        student_dict = dict(zip(columns, row))
        print(
            f"Student ID: {student_dict['id']}, Name: {student_dict['name']}, Mail: {student_dict['mail']}")
