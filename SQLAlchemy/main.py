from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/test", echo=True)

try:
    conn = engine.connect()
    result = conn.execute(text("SELECT VERSION()")).fetchone()[0]
    print(f"Server version: {result}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)


Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    mail = Column(String(50))
    password = Column(String(20), default="default_password")


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_student(session, name, mail=None, password=None):
    try:
        student = Student(name=name, mail=mail, password=password)
        session.add(student)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()


def get_student(session, name):
    try:
        student = session.query(Student).filter_by(name=name).first()
        return student
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_course(session, name):
    try:
        course = Course(name=name)
        session.add(course)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()


def get_course(session, name):
    try:
        course = session.query(Course).filter_by(name=name).first()
        return course
    except Exception as e:
        print(f"Error: {e}")
        return None


def close(session):
    session.close()


add_student(session, "John", "john@buaa.edu.cn", "123456")
add_course(session, "Math")

RED = "\033[91m"
END = "\033[0m"
student = get_student(session, "John")
print(f"{RED}Student: {student.name}, {student.mail}, {student.password}{END}")

course = get_course(session, "Math")
print(f"{RED}Course: {course.name}{END}")

close(session)
