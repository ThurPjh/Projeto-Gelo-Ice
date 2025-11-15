from datetime import datetime
from database import SessionLocal
from models import Produto

db = SessionLocal()


produto8 = Produto(nome="Coco", preco=3.00, quantidade=30, tipo="saborizado")
produto9 = Produto(nome="Maçã Verde", preco=3.00, quantidade=30, tipo="saborizado")
produto10 = Produto(nome="Maracujá", preco=3.00, quantidade=30, tipo="saborizado")
produto11 = Produto(nome="Limão e Gengibre", preco=3.00, quantidade=30, tipo="saborizado")
produto12 = Produto(nome="Cerveja", preco=3.00, quantidade=30, tipo="saborizado")
produto13 = Produto(nome="Beats Red Mix", preco=3.00, quantidade=30, tipo="saborizado")
produto14 = Produto(nome="Beats Sense", preco=3.00, quantidade=30, tipo="saborizado")
produto15 = Produto(nome="Beats GT", preco=3.00, quantidade=30, tipo="saborizado")
produto16 = Produto(nome="Laranja", preco=3.00, quantidade=30, tipo="saborizado")



db.add_all([produto8, produto9, produto10, produto11, produto12, produto13, produto14, produto15, produto16])
db.commit()
db.close()
