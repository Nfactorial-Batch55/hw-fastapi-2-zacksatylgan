from fastapi import FastAPI, Request, Response, HTTPException, Query
from fastapi.templating import Jinja2Templates

from .users import create_users

users = create_users(100)  # Здесь хранятся список пользователей
app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# (сюда писать решение)
# (конец решения)

@app.get("/users")
def get_users(request: Request, page: int = 1, per_page: int = 10):
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]
    total_pages = (len(users) + per_page - 1) // per_page  # Вычисляем общее количество страниц
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": paginated_users,
            "page": page,
            "total_pages": total_pages
        }
    )

@app.get("/users/{id}")
def get_user(request: Request, id: int):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})