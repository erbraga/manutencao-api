from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from database import db
from models import Manutencao

app = Flask(__name__)


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
    registros = Manutencao.query.all()
    return jsonify([r.to_dict() for r in registros])

# Rota para salvar novo registro
@app.route('/salvar', methods=['POST'])
def salvar():
    data = request.json
    novo = Manutencao(
        nome_peca=data.get("nome_peca"),
        intervalo_km=data.get("intervalo_km"),
        intervalo_periodo=data.get("intervalo_periodo"),
        historico_km=data.get("historico_km"),
        historico_periodo=data.get("historico_periodo"),
        revisao_km=data.get("revisao_km"),
        revisao_periodo=data.get("revisao_periodo")
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"message": "Registro salvo com sucesso!"}), 201

# Rota para editar registro
@app.route('/editar/<int:id>', methods=['PUT'])
def editar(id):
    data = request.json
    registro = Manutencao.query.get_or_404(id)

    registro.nome_peca = data.get("nome_peca", registro.nome_peca)
    registro.intervalo_km = data.get("intervalo_km", registro.intervalo_km)
    registro.intervalo_periodo = data.get("intervalo_periodo", registro.intervalo_periodo)
    registro.historico_km = data.get("historico_km", registro.historico_km)
    registro.historico_periodo = data.get("historico_periodo", registro.historico_periodo)
    registro.revisao_km = data.get("revisao_km", registro.revisao_km)
    registro.revisao_periodo = data.get("revisao_periodo", registro.revisao_periodo)

    db.session.commit()
    return jsonify({"message": "Registro atualizado com sucesso!"})

# Rota para deletar registro
@app.route('/del/<int:id>', methods=['DELETE'])
def deletar(id):
    registro = Manutencao.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return jsonify({"message": "Registro deletado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
