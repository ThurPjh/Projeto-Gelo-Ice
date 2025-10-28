from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form

#esse codigo funciona a base da fé, por favor tenha fé que o codigo vá funcionar!!! 🙏

app = FastAPI()

templates = Jinja2Templates(directory="templetes")

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post ("/login")
def login_post(username: str = Form("username"), password: str = Form("password")):
    if username == "admin" and password == "123":
        return {"message": "Login bem-sucedido!"}
    else:
        return {"message": "Login mal-sucedido!"}
