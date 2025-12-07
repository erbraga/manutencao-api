from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from datetime import datetime

from database import db
from models import Itens, Veiculo

app = Flask(__name__)
swagger = Swagger(app)


# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manutencao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Rota para recuperar os registros
@app.route('/recuperar', methods=['GET'])
def recuperar():
    '''Retorna todo o banco de dados cadastrado.
    ---

    responses:
      200:
        description: Retorna a lista de todos os itens de manutnção cadastrados no banco de dados
    '''

    itens= [item.to_dict() for item in Itens.query.all()]
    veiculo = [veiculo.to_dict() for veiculo in Veiculo.query.all()]
    
    return jsonify({'veiculo':veiculo,
                    'itens':itens})


# Rota para salvar novo item de manutenção
@app.route('/salvar', methods=['POST'])
def salvar():

    '''Salva novo item de manutenção no banco de dados
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Óleo do motor
            intervalo_km:
              type: integer
              example: 10000
            intervalo_prazo:
              type: integer
              example: 12
            ultima_troca_km:
              type: integer
              example: 10000
            ultima_troca_data:
              type: string
              format: date
              example: "2023-12-04"
            proxima_troca_km:
              type: integer
              example: 20000
            proxima_troca_data:
              type: string
              format: date
              example: "2024-11-25"
            veiculo:
              type: int
              example: 1
    responses:
      201:
        description: Registro salvo com sucesso!
    '''

    dados_recebidos = request.json
    novo_registro = Itens(
        descricao=dados_recebidos.get('descricao'),
        intervalo_km=dados_recebidos.get('intervalo_km'),
        intervalo_prazo=dados_recebidos.get('intervalo_prazo'),
        ultima_troca_km=dados_recebidos.get('ultima_troca_km'),
        ultima_troca_data=datetime.strptime(dados_recebidos['ultima_troca_data'],
                                            '%Y-%m-%d').date(),
        proxima_troca_km=dados_recebidos.get('ultima_troca_km'),
        proxima_troca_data=datetime.strptime(dados_recebidos['ultima_troca_data'],
                                            '%Y-%m-%d').date(),
        veiculo=dados_recebidos.get('veiculo'),
    )
    db.session.add(novo_registro)
    db.session.commit()
    return jsonify({'mensagem': 'Registro salvo com sucesso!'}), 201


# Rota para editar registro
@app.route('/alterar-item/<int:id>', methods=['PUT'])
def alterar_item(id):
    '''Altera um item de manutenção no banco de dados
    ---
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do item
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Óleo do motor
            intervalo_km:
              type: integer
              example: 10000
            intervalo_prazo:
              type: integer
              example: 12
            ultima_troca_km:
              type: integer
              example: 10000
            ultima_troca_data:
              type: string
              format: date
              example: "2023-12-04"
            proxima_troca_km:
              type: integer
              example: 20000
            proxima_troca_data:
              type: string
              format: date
              example: "2024-11-25"
            veiculo:
              type: int
              example: 1
    responses:
      201:
        description: Registro atualizado com sucesso!
    '''

    dados_recebidos = request.json
    registro = Itens.query.get_or_404(id)

    registro.descricao = dados_recebidos.get('descricao', registro.descricao)
    registro.intervalo_km = dados_recebidos.get('intervalo_km', registro.intervalo_km)
    registro.intervalo_prazo = dados_recebidos.get('intervalo_prazo', registro.intervalo_prazo)
    registro.ultima_troca_km = dados_recebidos.get('ultima_troca_km', registro.ultima_troca_km)
    registro.ultima_troca_data = datetime.strptime(dados_recebidos['ultima_troca_data'],
                                          '%Y-%m-%d').date()
    registro.proxima_troca_km = dados_recebidos.get('proxima_troca_km', registro.proxima_troca_km)
    registro.proxima_troca_data = datetime.strptime(dados_recebidos['proxima_troca_data'],
                                          '%Y-%m-%d').date()
    registro.veiculo = dados_recebidos.get('veiculo', registro.veiculo)
    db.session.commit()
    return jsonify({'mensagem': 'Registro atualizado com sucesso!'})


# Rota para deletar registro
@app.route('/deletar/<int:id>', methods=['DELETE'])
def deletar(id):
    '''Deleta o registro no banco de dados
    ---
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do item

    responses:
      200:
        description: Registro deletado com sucesso!
      404:
        description: Registro não encontrado!
    '''

    registro = Itens.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return jsonify({'mensagem': 'Registro deletado com sucesso!'})


# Rota para editar veiculo
@app.route('/alterar-veiculo/<int:id>', methods=['PUT'])
def alterar_veiculo(id):
    '''Altera um veiculo no banco de dados
    ---
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do veículo
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Ferrari F40
    responses:
      201:
        description: Registro atualizado com sucesso!
      404:
        description: Registro não encontrado
    '''

    dados_recebidos = request.json
    registro = Veiculo.query.get_or_404(id)

    registro.descricao = dados_recebidos.get('descricao', registro.descricao)
    db.session.commit()
    return jsonify({'mensagem': 'Registro atualizado com sucesso!'})


if __name__ == '__main__':
    app.run(debug=True)
