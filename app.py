import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, send_from_directory
from flask_cors import CORS

# Configuração do Flask
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'cotacoes.db')

def init_db():
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

# ROTA PARA O SITE
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ROTA PARA SALVAR DADOS
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

# DASHBOARD DE CLIENTES (Acesse: seu-site.onrender.com/leads)
@app.route('/leads')
def ver_leads():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cotacoes ORDER BY data_envio DESC')
        leads = cursor.fetchall()
        total = len(leads)
        conn.close()

        html_template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Admin | BsProtector</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <nav class="navbar navbar-dark bg-primary mb-4"><div class="container"><span class="navbar-brand">Leads BsProtector</span></div></nav>
            <div class="container">
                <h2>Lista de Cotações (Total: {{ total_leads }})</h2>
                <div class="card p-3">
                    <table class="table table-striped">
                        <thead><tr><th>Nome</th><th>Email</th><th>Telefone</th><th>Seguro</th><th>Data</th></tr></thead>
                        <tbody>
                            {% for r in leads %}
                            <tr><td>{{ r[1] }}</td><td>{{ r[2] }}</td><td>{{ r[3] }}</td><td>{{ r[4] }}</td><td>{{ r[6] }}</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <br><a href="/" class="btn btn-secondary">Voltar ao Site</a>
            </div>
        </body>
        </html>
        '''
        return render_template_string(html_template, leads=leads, total_leads=total)
    except Exception as e:
        return f"Erro: {e}"

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)