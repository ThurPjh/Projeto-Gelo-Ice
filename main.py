from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import AuthUser

app = FastAPI()

templates = Jinja2Templates(directory="templetes")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_post(
    username: str = Form(...),  # 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if AuthUser(db, username, password):
        return RedirectResponse(url="/", status_code=303)
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário ou senha inválidos"},
            status_code=401
        )
