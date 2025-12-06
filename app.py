from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from datetime import datetime

from database import db
from models import Itens

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

# Rota para listar registros
@app.route('/listar', methods=['GET'])
def listar():
    """Retorna todos os ítens cadastrados.
    ---

    responses:
      200:
        description: Retorna a lista de todos os itens de manutnção cadastrados no banco de dados
    """
    registros = Itens.query.all()
    return jsonify([r.to_dict() for r in registros])

# Rota para salvar novo registro
@app.route('/salvar', methods=['POST'])
def salvar():

    """Salva o registro no banco de dados
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
            intervalo_km:
              type: integer
            intervalo_prazo:
              type: integer
            ultima_troca_km:
              type: integer
            ultima_troca_data:
              type: string
              format: date
              example: "2025-12-04"
            proxima_troca_km:
              type: integer
            proxima_troca_data:
              type: string
              format: date
              example: "2025-12-04"
            veiculo:
              type: int
    responses:
      201:
        description: Registro salvo com sucesso!
    """
    data = request.json
    novo = Itens(
        descricao=data.get("descricao"),
        intervalo_km=data.get("intervalo_km"),
        intervalo_prazo=data.get("intervalo_prazo"),
        ultima_troca_km=data.get("ultima_troca_km"),
        ultima_troca_data=datetime.strptime(data["ultima_troca_data"],
                                            "%Y-%m-%d").date(),
        proxima_troca_km=data.get("ultima_troca_km"),
        proxima_troca_data=datetime.strptime(data["ultima_troca_data"],
                                            "%Y-%m-%d").date(),
        veiculo=data.get("veiculo"),
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Registro salvo com sucesso!"}), 201

# Rota para editar registro
@app.route('/editar/<int:id>', methods=['PUT'])
def editar(id):
    """Altera o registro no banco de dados
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
            intervalo_km:
              type: integer
            intervalo_prazo:
              type: integer
            ultima_troca_km:
              type: integer
            ultima_troca_data:
              type: string
              format: date
              example: "2025-12-04"
            proxima_troca_km:
              type: integer
            proxima_troca_data:
              type: string
              format: date
              example: "2025-12-04"
            veiculo:
              type: int
    responses:
      201:
        description: Registro atualizado com sucesso!
    """

    data = request.json
    registro = Itens.query.get_or_404(id)

    registro.descricao = data.get("descricao", registro.descricao)
    registro.intervalo_km = data.get("intervalo_km", registro.intervalo_km)
    registro.intervalo_prazo = data.get("intervalo_prazo", registro.intervalo_prazo)
    registro.ultima_troca_km = data.get("ultima_troca_km", registro.ultima_troca_km)
    registro.ultima_troca_data = datetime.strptime(data["ultima_troca_data"],
                                          "%Y-%m-%d").date()
    registro.proxima_troca_km = data.get("proxima_troca_km", registro.proxima_troca_km)
    registro.proxima_troca_data = datetime.strptime(data["proxima_troca_data"],
                                          "%Y-%m-%d").date()
    registro.veiculo = data.get("veiculo", registro.veiculo)
    db.session.commit()
    return jsonify({"message": "Registro atualizado com sucesso!"})

# Rota para deletar registro
@app.route('/del/<int:id>', methods=['DELETE'])
def deletar(id):
    """Deleta o registro no banco de dados
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
        description: Registro salvo com sucesso!
      404:
        description: Registro não encontrado!
    """

    registro = Itens.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return jsonify({"message": "Registro deletado com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True)
