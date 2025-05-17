import sqlite3
from dotenv import load_dotenv
import os
import re

# Carrega variáveis de ambiente
load_dotenv()

# Função para extrair o caminho do banco de dados da URI SQLite
def parse_sqlite_uri(uri):
    if uri and uri.startswith('sqlite:///'):
        # Extrai o caminho do arquivo do banco de dados
        db_path = uri[10:]  # Remove 'sqlite:///'
        return db_path
    return None

# Obtém a URI do banco de dados
db_uri = os.getenv('DATABASE_URI')
print(f"URI obtida do arquivo .env: {db_uri}")

# Extrai o caminho do banco de dados
db_path = parse_sqlite_uri(db_uri)
print(f"Caminho do banco de dados SQLite: {db_path}")

if not db_path:
    print("Erro: URI do banco de dados inválida. Deve ser no formato 'sqlite:///nome_do_arquivo.db'")
    exit(1)

# Cria o banco de dados SQLite
try:
    print(f"Criando/conectando ao banco de dados SQLite: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cria as tabelas necessárias (só para garantir que o arquivo seja criado)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    
    # Fecha a conexão
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n=== Configuração do banco de dados SQLite concluída com sucesso! ===")
    print(f"Banco de dados criado em: {os.path.abspath(db_path)}")
    print("Você pode iniciar a aplicação executando: python app.py")
    
except sqlite3.Error as err:
    print(f"\n=== ERRO ao criar o banco de dados SQLite: {err} ===")
    exit(1)
