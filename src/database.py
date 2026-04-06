# Funções de acesso ao SQLite
import sqlite3

# conecta com o bando de dados utilizando WAL
def get_db_connection():
    conn = sqlite3.connect('dados.db', timeout=10)
    conn.execute('PRAGMA journal_mode=WAL') 
    conn.execute('PRAGMA busy_timeout=5000')
    conn.row_factory = sqlite3.Row
    return conn

# inicializa o banco de dados e cria a tabela se não existir
def init_db():
    with get_db_connection() as conn:
        with open('src/schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())

# insere uma nova leitura no banco
def inserir_leitura(temp, umid, pressao=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)",
                (temp, umid, pressao))
    id_novo = cur.lastrowid
    conn.commit()
    conn.close()
    return id_novo

# pega as estatisticas de maximo minimo e media da temperatura
def obter_estatisticas():
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT 
            AVG(temperatura) as media, 
            MIN(temperatura) as min, 
            MAX(temperatura) as max 
        FROM leituras
    ''').fetchone()
    conn.close()
    return stats

# lista as 50 leituras mais recentes, com paginação
def listar_leituras(limite=50, offset=0):
    conn = get_db_connection()
    leituras = conn.execute(
        'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ? OFFSET ?', (limite, offset)
    ).fetchall()
    conn.close()
    return leituras

# busca uma leitura específica pelo ID
def buscar_leitura(id):
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    return leitura

# atualiza uma leitura existente no banco
def atualizar_leitura(id, temp, umid, pressao=None):
    conn = get_db_connection()
    conn.execute(
        'UPDATE leituras SET temperatura = ?, umidade = ?, pressao = ? WHERE id = ?',
        (temp, umid, pressao, id)
    )
    conn.commit()
    conn.close()

#deleta uma leitura do banco
def deletar_leitura(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    conn.close()