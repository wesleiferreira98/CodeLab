from flask import Flask, jsonify, render_template, request
from intepretador_server import SessaoInterpretador
import os

app = Flask(__name__)
sessoes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/desafios.html')
def desafios():
    return render_template('desafios.html')
@app.route('/executar', methods=['POST'])
def executar_codigo():
    dados = request.json
    sessao_id = dados.get('sessao_id')
    codigo = dados.get('codigo', '')
    
    if sessao_id not in sessoes:
        sessoes[sessao_id] = SessaoInterpretador(sessao_id)
        
    return sessoes[sessao_id].processar_codigo(codigo)

@app.route('/input', methods=['POST'])
def processar_input():
    dados = request.json
    sessao_id = dados.get('sessao_id')
    valor = dados.get('valor', '')
    
    if sessao_id not in sessoes:
        return jsonify({'erro': 'Sessão inválida'}), 400
        
    return sessoes[sessao_id].processar_input(valor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
