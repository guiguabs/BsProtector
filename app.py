import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, send_from_directory
from flask_cors import CORS

# Configura o Flask
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

# COMANDO CRUCIAL: Inicializa o banco assim que o arquivo é lido pelo Render
init_db()

# ROTA PARA MOSTRAR O SITE
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
        return f"Erro: {e}"

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
            <style>
                body { background: #f8f9fa; padding: 20px; }
                .table-card { background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); padding: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>Leads BsProtector (Total: {{ total_leads }})</h2>
                    <form action="/limpar_banco" method="POST" onsubmit="return confirm('Apagar todos os leads?')">
                        <button type="submit" class="btn btn-danger">Limpar Banco</button>
                    </form>
                </div>
                <div class="table-card">
                    <table class="table table-hover">
                        <thead><tr><th>Nome</th><th>Email</th><th>Telefone</th><th>Seguro</th><th>Data</th></tr></thead>
                        <tbody>
                            {% for r in leads %}
                            <tr>
                                <td>{{ r[1] }}</td>
                                <td>{{ r[2] }}</td>
                                <td>{{ r[3] }}</td>
                                <td>{{ r[4] }}</td>
                                <td>{{ r[6] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <br><a href="/" class="btn btn-primary">Voltar ao Site</a>
            </div>
        </body>
        </html>
        '''
        return render_template_string(html_template, leads=dados, total_leads=total)
    except Exception as e:
        return f"Erro: {e}"

# Para rodar localmente (opcional)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
