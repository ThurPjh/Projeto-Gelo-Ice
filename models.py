from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, joinedload
from database import Base
from datetime import datetime


data = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    tipo = Column(String, index=True)


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    endereco = Column(String(150))
    cep = Column(Integer)
    numero = Column(Integer)

class Caixa(Base):
    __tablename__ = "caixas"

    id_caixa = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    volume = Column(DECIMAL(10, 2), nullable=False) 
    status = Column(String(20), default="disponível")  

class Geladeira(Base):
    __tablename__ = "geladeiras"

    id_geladeira = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, nullable=False)  
    valor = Column(DECIMAL, nullable=False)
    marca = Column(String(50), nullable=False)
    formato = Column(String(50), nullable=False)
    status = Column(String(20), default="disponível")

    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=True)
    cliente = relationship("Cliente")



class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
    quantidade = Column(Integer, default=0)
    tipo = Column(String(50)) 


class Entrega(Base):
    __tablename__ = "entregas"

    id_entrega = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    status = Column(String(50), default="pago") 
    pago = Column(Boolean, default=False)          
    data = Column(DateTime, default=datetime.now)

    cliente = relationship("Cliente")
    itens = relationship("ItemEntrega", back_populates="entrega")


class ItemEntrega(Base):
    __tablename__ = "itens_entrega"

    id_item_entrega = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"), nullable=False)
    id_produto = Column(Integer, ForeignKey("produtos.id_produto"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    entrega = relationship("Entrega", back_populates="itens")
    produto = relationship("Produto")

class Aluguel(Base):
    __tablename__ = "alugueis"

    id_aluguel = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    data_prevista_devolucao = Column(Date)
    data_entrega = Column(Date)
    id_caixa = Column(Integer, ForeignKey("caixas.id_caixa"), nullable=False)
    id_geladeira = Column(Integer, ForeignKey("geladeiras.id_geladeira"), nullable=False)

    cliente = relationship("Cliente")
    caixa = relationship("Caixa")
    geladeira = relationship("Geladeira")

class Nota(Base):
    __tablename__ = "notas"

    id_nota = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"), nullable=True)
    id_aluguel = Column(Integer, ForeignKey("alugueis.id_aluguel"), nullable=True) 
    valor = Column(DECIMAL(10, 2), nullable=False)
    status_pagamento = Column(String(50))

    entrega = relationship("Entrega")
    aluguel = relationship("Aluguel")


