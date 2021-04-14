from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):

    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_tasks():
    # datetime.today().date()  # current date without time
    # today = datetime.today()
    # today.day  # the day of a current month.
    # today.strftime('%b')  # the short name of the current month. I.e 'Apr'

    today = datetime.today()
    print(f"Today {today, today.strftime('%b')}:")
    rows = session.query(Table).filter(Table.deadline == today.date()).all()

    if len(rows) == 0:
        print("""Today:
Nothing to do!""")
    else:
        print("Today:")
        print(rows)


def week_tasks():
    today = datetime.today()
    for i in range(0, 7):
        print(f"{datetime.strftime(today + timedelta(days=i), '%A %d %b')}:")
        day = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == day.date()).all()
        if len(rows) == 0:
            print("""Nothing to do!""")
            print()
        else:
            print(rows)
            print()


def all_tasks():
    print("All tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()

    if rows:
        for row in rows:
            day = (datetime.strftime(row.deadline, '%d %b'))
            print(f"{row.id}. {row}. {day}")
        print()
    else:
        print("Nothing to do!\n")


def missed_tasks():
    print("Missed tasks:")
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    print(rows)
    print()


def add_tasks():
    new_task = input("Enter task\n")
    new_row = Table(task=new_task)
    task_deadline = input("Enter deadline\n")
    new_row.deadline = datetime.strptime(task_deadline, '%Y-%m-%d')
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def delete_tasks():
    print("Choose the number of the task you want to delete:")
    rows = session.query(Table).order_by(Table.deadline).all()

    if rows:
        for row in rows:
            day = (datetime.strftime(row.deadline, '%d %b'))
            print(f"{row.id}. {row}. {day}")

        number_of_task = int(input())

        session.query(Table).filter(Table.id == number_of_task).delete()
        session.commit()

        print("The task has been deleted!\n")

    else:

        print("Nothing to delete!\n")


while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    user_choice = input()

    print()

    if user_choice == "1":
        today_tasks()  # Today's tasks
    elif user_choice == "2":
        week_tasks()  # Week's tasks
    elif user_choice == "3":
        all_tasks()  # All tasks
    elif user_choice == "4":
        missed_tasks()  # Missed tasks
    elif user_choice == "5":
        add_tasks()  # Add task
    elif user_choice == "6":
        delete_tasks()  # Delete task
    elif user_choice == "0":
        print("Bye!")
        break
