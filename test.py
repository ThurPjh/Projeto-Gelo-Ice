from database import engine

try:
    # Testa a conexão
    conn = engine.connect()
    print("Conexão com o banco OK!")
    conn.close()
except Exception as e:
    print("Erro na conexão:", e)