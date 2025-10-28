from database import engine, Base
import models  # importa todos os modelos

Base.metadata.create_all(bind=engine)
