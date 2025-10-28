from database import SessionLocal
from models import User
db = SessionLocal()

ronaldo = User(username="Ronaldo", tipo="ADM", password="quequeeledisse")
db.add(ronaldo)
db.commit()
db.close()