import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, send_from_directory
from flask_cors import CORS

# Configura o Flask para reconhecer a pasta atual para arquivos estáticos
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

# --- ROTA PARA MOSTRAR SEU SITE (O INDEX.HTML) ---
@app.route('/')
def index():
    try:
        # Tenta carregar o seu arquivo index.html
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return f"Erro ao carregar index.html: Certifique-se que o arquivo está na mesma pasta que o app.py"

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
            (dados.get('name'), dados.get('email'), dados.get('phone'), 
             dados.get('insurance-type'), dados.get('message')))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# ROTA PARA LIMPAR O BANCO
@app.route('/limpar_banco', methods=['POST'])
def limpar_banco():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cotacoes')
        conn.commit()
        conn.close()
        return redirect(url_for('ver_leads'))
    except Exception as e:
        return f"Erro ao limpar banco: {e}"

# DASHBOARD DE LEADS
@app.route('/leads')
def ver_leads():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cotacoes ORDER BY data_envio DESC')
        dados = cursor.fetchall()
        total = len(dados)
        conn.close()

        html_template = '''
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Admin | BsProtector</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                body { background: #f8f9fa; font-family: 'Segoe UI', sans-serif; }
                .navbar { background: #002d72; color: white; padding: 15px; }
                .container { margin-top: 30px; }
                .table-card { background: white; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 25px; }
                .badge-seguro { background: #e7f0ff; color: #0056b3; padding: 6px 15px; border-radius: 20px; font-weight: bold; }
            </style>
        </head>
        <body>
            <nav class="navbar"><div class="container-fluid"><span class="h4 mb-0">BsProtector Leads</span></div></nav>
            <div class="container">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                        <h2 class="fw-bold">Leads de Cotação</h2>
                        <span class="badge bg-dark">Total: {{ total_leads }}</span>
                    </div>
                    <form action="/limpar_banco" method="POST" onsubmit="return confirm('Apagar tudo?')">
                        <button type="submit" class="btn btn-danger">Limpar Banco</button>
                    </form>
                </div>
                <div class="table-card">
                    <table class="table table-hover">
                        <thead><tr><th>Cliente</th><th>Contato</th><th>Seguro</th><th>Data</th><th>Msg</th></tr></thead>
                        <tbody>
                            {% for r in leads %}
                            <tr>
                                <td>{{ r[1] }}</td>
                                <td>{{ r[2] }}<br>{{ r[3] }}</td>
                                <td><span class="badge-seguro">{{ r[4] }}</span></td>
                                <td>{{ r[6] }}</td>
                                <td><button onclick="alert('{{ r[5] }}')">Ver</button></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
        '''
        return render_template_string(html_template, leads=dados, total_leads=total)
    except Exception as e:
        return f"Erro: {e}"

if __name__ == '__main__':
    init_db()
    # O Render usa a porta 10000 por padrão, ou a variável de ambiente PORT
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)