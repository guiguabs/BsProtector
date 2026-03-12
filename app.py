import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Configura o Flask
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Banco no /tmp para permissao no Render
DB_PATH = '/tmp/cotacoes.db'

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT, email TEXT, telefone TEXT, tipo_seguro TEXT, mensagem TEXT,
                data_envio DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro no banco: {e}")

init_db()

# Rota principal para carregar o index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Rota para salvar os leads
@app.route('/salvar_cotacao', methods=['POST'])
def salvar_cotacao():
    try:
        dados = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cotacoes (nome, email, telefone, tipo_seguro, mensagem) 
            VALUES (?, ?, ?, ?, ?)''',
            (dados.get('nome'), dados.get('email'), dados.get('telefone'), 
             dados.get('tipo_seguro'), dados.get('mensagem')))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
