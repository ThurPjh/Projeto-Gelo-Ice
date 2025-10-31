from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import AuthUser
from models import Cliente, Entrega, Produto, ItemEntrega
from datetime import datetime


app = FastAPI()
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")


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

#PÀGINAS FINANCEIRO


@app.get("/financeiro", response_class=HTMLResponse)
def financeiro(request: Request):
    return templates.TemplateResponse("financeiro-main.html", {"request": request})

#PÀGINAS ESTOQUE

@app.get("/estoque", response_class=HTMLResponse)
def estoque(request: Request):
    return templates.TemplateResponse("estoque-main.html", {"request": request})

@app.get("/estoque-saborizado", response_class=HTMLResponse)
def estoque_saborizado(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.tipo == "saborizado").all()
    return templates.TemplateResponse("estoque-gelo-saborizado.html", {"request": request, "produtos": produtos})


@app.get("/estoque-gelo", response_class=HTMLResponse)
def estoque_gelo(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.tipo == "gelo").all()
    return templates.TemplateResponse("estoque-gelo.html", {"request": request, "produtos": produtos})


#PÀGINAS CLIENTES

@app.get("/clientes", response_class=HTMLResponse)
def clientes(request: Request, db: Session = Depends(get_db)):
    lista_clientes = db.query(Cliente).all()
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": lista_clientes})

#PÀGINAS ENTREGAS

@app.get("/entrega", response_class=HTMLResponse)
def entrega(request: Request):
    return templates.TemplateResponse("entregas-main.html", {"request": request})

@app.get("/entregas-registro", response_class=HTMLResponse)
def entregas_registro(request: Request, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    produtos = db.query(Produto).all()
    return templates.TemplateResponse("entregas-registro.html", {"request": request, "clientes": clientes, "produtos": produtos})


@app.get("/entregas-historico", response_class=HTMLResponse)
def entregas_historico(request: Request):
    return templates.TemplateResponse("entregas-historico.html", {"request": request})



# ADICIONAR CLIENTES NO BD


@app.post("/clientes/adicionar")
def adicionar_cliente(
    nome: str = Form(...),
    telefone: str = Form(""),
    endereco: str = Form(""),
    db: Session = Depends(get_db)
):
    novo_cliente = Cliente(
        nome=nome,
        telefone=telefone,
        endereco=endereco,
    )
    db.add(novo_cliente)
    db.commit()
    return RedirectResponse(url="/clientes", status_code=303)


#REGISTRAR ENTREGA 

@app.post("/entregas/registrar")
def registrar_entrega(
    id_cliente: int = Form(...),
    nota: str = Form(None),
    pago_na_hora: str = Form(None),
    db: Session = Depends(get_db),
    request: Request = None
):
    # Criar entrega
    entrega = Entrega(id_cliente=id_cliente, status="registrada")
    db.add(entrega)
    db.commit()
    db.refresh(entrega)

    # Capturar produtos entregues
    produtos = db.query(Produto).all()
    for produto in produtos:
        quantidade = int(request.form().get(f"produto_{produto.id_produto}", 0))
        if quantidade > 0:
            item = ItemEntrega(id_entrega=entrega.id_entrega, id_produto=produto.id_produto, quantidade=quantidade)
            db.add(item)

    db.commit()
    return RedirectResponse(url="/entregas-historico", status_code=303)

#ADICIONAR ESTOQUE

@app.post("/estoque/adicionar")
def adicionar_estoque(
    id_produto: int = Form(...),
    quantidade: int = Form(...),
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if produto:
        produto.quantidade += quantidade
        db.commit()

        # Redireciona para a página correta com base no tipo
        if produto.tipo == "saborizado":
            return RedirectResponse(url="/estoque-saborizado", status_code=303)
        else:
            return RedirectResponse(url="/estoque-gelo", status_code=303)

    # Se o produto não for encontrado, volta para a página principal
    return RedirectResponse(url="/estoque", status_code=303)






