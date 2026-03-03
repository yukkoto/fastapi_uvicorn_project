from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
import re


my_app = FastAPI(title="FastAPI KR1 — Контрольная работа №1")


@my_app.get("/")
def root():
    return {"message": "Авторелоад действительно работает"}



@my_app.get("/html", response_class=FileResponse)
def get_html():
    return FileResponse("index.html")



class CalcInput(BaseModel):
    num1: float
    num2: float


@my_app.post("/calculate")
def calculate(data: CalcInput):
    return {"result": data.num1 + data.num2}



from models import User

current_user = User(name="Иван Иванов", id=1)


@my_app.get("/users")
def get_users():
    return current_user



class UserAge(BaseModel):
    name: str
    age: int


@my_app.post("/user")
def check_adult(user: UserAge):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18,
    }




class Feedback(BaseModel):
    name: str
    message: str


feedbacks_simple: list = []


@my_app.post("/feedback")
def submit_feedback(feedback: Feedback):
    feedbacks_simple.append({"name": feedback.name, "message": feedback.message})
    return {"message": f"Feedback received. Thank you, {feedback.name}."}


@my_app.get("/feedbacks")
def get_feedbacks():
    return feedbacks_simple



BANNED_WORDS = ["кринж", "рофл", "вайб"]


class FeedbackValidated(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def no_banned_words(cls, v: str) -> str:
        text_lower = v.lower()
        for word in BANNED_WORDS:
            root = word[:4]
            if re.search(root, text_lower):
                raise ValueError("Использование недопустимых слов")
        return v


feedbacks_validated: list = []


@my_app.post("/feedback/validated")
def submit_feedback_validated(feedback: FeedbackValidated):
    feedbacks_validated.append({"name": feedback.name, "message": feedback.message})
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}