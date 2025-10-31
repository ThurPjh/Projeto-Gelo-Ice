from datetime import datetime
from database import SessionLocal
from models import Produto

db = SessionLocal()


produto1 = Produto(nome="Cubo 2kg", preco=4.50, quantidade=50, tipo="gelo")
produto2 = Produto(nome="Cubo 4kg", preco=7.00, quantidade=500, tipo="gelo")
produto3 = Produto(nome="Cubo 10kg", preco=15.00, quantidade=10, tipo="gelo")
produto4 = Produto(nome="Barra 10kg", preco=10.00, quantidade=300, tipo="gelo")


produto5 = Produto(nome="Limão", preco=3.00, quantidade=30, tipo="saborizado")
produto6 = Produto(nome="Morango", preco=3.00, quantidade=30, tipo="saborizado")
produto7 = Produto(nome="Melancia", preco=3.00, quantidade=30, tipo="saborizado")


db.add_all([produto1, produto2, produto3, produto4, produto5, produto6, produto7])
db.commit()
db.close()
