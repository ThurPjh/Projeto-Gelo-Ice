from sqlalchemy.orm import Session
from models import User

def AuthUser(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if user.password != password:
        return None
    return user