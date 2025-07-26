from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import sessionmaker
from models import AppUser, Task, Base


class TaskManagerDB:
    def __init__(self, path="sqlite:///activities.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def user_exists(self, email) -> bool:
        return self.session.query(AppUser).filter_by(email=email).first() is not None

    def add_user(self, name: str, email: str, password: str) -> str:
        if self.user_exists(email):
            return "It seems this email has been used before"
        try:
            new_user = AppUser(name=name, email=email, password=password)
            self.session.add(new_user)
            self.session.commit()
            return "Account created successfully"
        except Exception as e:
            self.session.rollback()
            return f"Error creating account: {e}"

    def get_user(self, user_id: int):
        return self.session.get(AppUser, user_id)

    def find_user_by_email(self, email: str):
        return self.session.query(AppUser).filter_by(email=email).first()

    def get_users(self):
        return self.session.scalars(select(AppUser)).all()

    def add_task(self, title: str, description: str, user_id: int):
        try:
            new_task = Task(title=title, description=description, user_id=user_id)
            self.session.add(new_task)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error adding task: {e}")

    def get_task(self, task_id: int):
        task = self.session.get(Task, task_id)
        if not task:
            raise Exception(f"Task with ID {task_id} not found")
        return task

    def find_tasks_by_user_id(self, user_id: int):
        return self.session.query(Task).filter_by(user_id=user_id).all()

    def search_tasks_by_name(self, title_fragment: str):
        return self.session.query(Task).filter(Task.title.ilike(f"%{title_fragment}%")).all()

    def update_task(self, task_id: int, new_title: str, new_description: str, new_status: str):
        task = self.session.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}
        task.title = new_title
        task.description = new_description
        task.status = new_status
        self.session.commit()
        self.session.refresh(task)
        return task

    def update_user(self, user_id: int, new_name: str):
        user = self.session.get(AppUser, user_id)
        if not user:
            raise Exception("User not found")
        user.name = new_name
        self.session.commit()
        self.session.refresh(user)
        return user

    def remove_user(self, user_id: int):
        result = self.session.execute(
            delete(AppUser).where(AppUser.id == user_id)
        ).rowcount
        self.session.commit()
        if result == 0:
            raise Exception(f"No user with ID {user_id} found.")

    def remove_task(self, task_id: int):
        result = self.session.execute(
            delete(Task).where(Task.id == task_id)
        ).rowcount
        self.session.commit()
        if result == 0:
            raise Exception(f"No task with ID {task_id} found.")
