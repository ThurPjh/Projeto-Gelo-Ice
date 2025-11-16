from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import Session, relationship, joinedload
from datetime import datetime
from database import SessionLocal
from auth import AuthUser
from models import Cliente, Entrega, Produto, ItemEntrega, Aluguel, Geladeira, Caixa, Nota
from typing import Optional


data = Column(DateTime, default=datetime.now)
app = FastAPI()


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
    request: Request,
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

@app.get("/financeiro-notas", response_class=HTMLResponse)
def financeiro_notas(request: Request, db: Session = Depends(get_db)):
    entregas = db.query(Entrega).options(
        joinedload(Entrega.itens).joinedload(ItemEntrega.produto),
        joinedload(Entrega.cliente)
    ).order_by(Entrega.data.desc()).all()
    return templates.TemplateResponse("financeiro-notas.html", {"request": request, "entregas": entregas})

#PÀGINAS ESTOQUE

@app.get("/estoque", response_class=HTMLResponse)
def estoque(request: Request):
    return templates.TemplateResponse("estoque-main.html", {"request": request})

@app.get("/estoque-saborizado", response_class=HTMLResponse)
def estoque_saborizado(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.tipo == "saborizado").order_by(Produto.quantidade.desc()).all()
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
    produtos = db.query(Produto).order_by(Produto.id_produto.asc()).all()
    return templates.TemplateResponse("entregas-registro.html", {"request": request, "clientes": clientes, "produtos": produtos})


@app.get("/entregas-historico")
def entregas_historico(request: Request, db: Session = Depends(get_db)):
    entregas = db.query(Entrega).order_by(Entrega.data.desc()).all()
    return templates.TemplateResponse("entregas-historico.html", {"request": request, "entregas": entregas})

# PÀGINAS ALUGUEIS

@app.get("/alugueis", response_class=HTMLResponse)
def alugueis(request: Request):
    return templates.TemplateResponse("alugueis-main.html", {"request": request})

@app.get("/caixas", response_class=HTMLResponse)
def caixas(request: Request, db: Session = Depends(get_db)):
    caixas = db.query(Caixa).order_by(Caixa.numero.asc()).all()
    return templates.TemplateResponse("caixas.html", {"request": request, "caixas": caixas})

@app.get("/geladeiras")
def listar_geladeiras(request: Request, db: Session = Depends(get_db)):
    geladeiras = db.query(Geladeira).all()
    return templates.TemplateResponse(
        "geladeiras.html",
        {"request": request, "geladeiras": geladeiras}
    )


# ADICIONAR CLIENTES NO BD


@app.post("/clientes/adicionar")
def adicionar_cliente(
    nome: str = Form(...),
    telefone: str = Form(""),
    endereco: str = Form(""),
    cep: int = Form(...),
    numero: int = Form(...),
    db: Session = Depends(get_db)
):
    novo_cliente = Cliente(
        nome=nome,
        telefone=telefone,
        endereco=endereco,
        cep=cep,
        numero=numero
    )
    db.add(novo_cliente)
    db.commit()
    return RedirectResponse(url="/clientes", status_code=303)


#REGISTRAR ENTREGA 

@app.post("/entregas/registrar")
async def registrar_entrega(
    request: Request,
    id_cliente: int = Form(...),
    nota: str = Form(None),
    pago_na_hora: str = Form(None),
    db: Session = Depends(get_db)
):
    # status da entrega
    status = "nota" if nota == "true" else "normal"
    pago = True if pago_na_hora == "true" else False

    # cria entrega
    entrega = Entrega(id_cliente=id_cliente, status=status, pago=pago)
    db.add(entrega)
    db.commit()
    db.refresh(entrega)

    # adiciona itens da entrega e calcula valor total
    form_data = await request.form()
    valor_total = 0
    for key, value in form_data.items():
        if key.startswith("produto_"):
            id_produto = int(key.replace("produto_", ""))
            quantidade = int(value)
            if quantidade > 0:
                produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
                if produto:
                    valor_total += float(produto.preco) * quantidade
                item = ItemEntrega(
                    id_entrega=entrega.id_entrega,
                    id_produto=id_produto,
                    quantidade=quantidade
                )
                db.add(item)

    db.commit()

    # sempre cria uma nota, independente de pago ou não
    nova_nota = Nota(
    id_entrega=entrega.id_entrega,
    id_aluguel=None,  
    valor=valor_total,
    status_pagamento="pago" if pago else "pendente"
    )
    db.add(nova_nota)
    db.commit()


    return RedirectResponse("/entregas-historico", status_code=303)




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

#ADICIONAR CAIXA

@app.post("/caixas/adicionar")
def adicionar_caixa(
    numero: int = Form(...), 
    valor: float = Form(...), 
    volume: float = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)):
    nova_caixa = Caixa(numero=numero, valor=valor, volume=volume, status=status)
    db.add(nova_caixa)
    db.commit()
    return RedirectResponse("/caixas", status_code=303)

#ADICIONAR FREEZER-

@app.post("/geladeiras/adicionar")
def adicionar_geladeira(
    numero: int = Form(...),
    valor: float = Form(...),
    marca: str = Form(...),
    formato: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    nova_geladeira = Geladeira(
        numero=numero,
        valor=valor,
        marca=marca,
        formato=formato,
        status=status
    )
    db.add(nova_geladeira)
    db.commit()
    return RedirectResponse("/geladeiras", status_code=303)

#MARCAR ENTREGA COMO PAGA

@app.post("/entregas/{id_entrega}/pagar")
def marcar_como_pago(id_entrega: int, db: Session = Depends(get_db)):
    entrega = db.query(Entrega).filter(Entrega.id_entrega == id_entrega).first()
    if entrega:
        entrega.pago = True
        entrega.status = "pago"

        # Atualiza também a nota vinculada
        nota = db.query(Nota).filter(Nota.id_entrega == id_entrega).first()
        if nota:
            nota.status_pagamento = "pago"

        db.commit()
    return RedirectResponse("/entregas-historico", status_code=303)



