from database import SessionLocal
from models import Cliente
from datetime import datetime
db = SessionLocal()

cliente1 = Cliente(nome="Sr Claudio", data_cadastro=datetime.now())
cliente2 = Cliente(nome="Sr Cladiu", data_cadastro=datetime.now())
cliente3 = Cliente(nome="Sr Claudia", data_cadastro=datetime.now())
cliente4 = Cliente(nome="Sr thungado", data_cadastro=datetime.now())
cliente5 = Cliente(nome="Sr thung life", data_cadastro=datetime.now())

db.add_all([cliente1, cliente2, cliente3, cliente4, cliente5])
db.commit()
db.close()