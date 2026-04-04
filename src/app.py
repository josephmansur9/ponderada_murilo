# Aplicação Flask principal
from flask import Flask, render_template, request, jsonify, redirect, url_for
import database

app = Flask(__name__)

@app.route('/')
def index():
    dados = database.listar_leituras(10)
    if request.args.get('formato') == 'json':
        return jsonify([dict(ix) for ix in dados])
    return render_template('index.html', leituras=dados)

@app.route('/leituras', methods=['GET', 'POST'])
def listar_ou_criar():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        dados = request.get_json()
        if not dados:
            return jsonify({'error': 'No JSON received'}), 400
        id_novo = database.inserir_leitura(
            dados.get('temperatura'),
            dados.get('umidade'),
            dados.get('pressao')
        )
        return jsonify({'id': id_novo, 'status': 'criado'}), 201

    dados = database.listar_leituras()
    return render_template('historico.html', leituras=dados)

@app.route('/leituras/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_leitura(id):
    if request.method == 'GET':
        leitura = database.buscar_leitura(id)
        return render_template('editar.html', leitura=leitura)
    
    if request.method == 'PUT':
        dados = request.get_json()
        database.atualizar_leitura(id, dados['temperatura'], dados['umidade'])
        return jsonify({'status': 'atualizado'})

    if request.method == 'DELETE':
        database.deletar_leitura(id)
        return jsonify({'status': 'removido'})
    
@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    stats = database.obter_estatisticas()
    if stats:
        return jsonify({
            'media': round(stats['media'], 2),
            'minimo': stats['min'],
            'maximo': stats['max']
        })
    return jsonify({'erro': 'Sem dados disponíveis'}), 404


# Error handlers for debugging
@app.errorhandler(400)
def bad_request(e):
    return f"400 Bad Request: {e}", 400

@app.errorhandler(403)
def forbidden(e):
    return f"403 Forbidden: {e}", 403

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True, port=5001)