from database import db

# Modelo da tabela
class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_peca = db.Column(db.String(100), nullable=False)
    intervalo_km = db.Column(db.Integer, nullable=True)
    intervalo_periodo = db.Column(db.String(50), nullable=True)
    historico_km = db.Column(db.Integer, nullable=True)
    historico_periodo = db.Column(db.String(50), nullable=True)
    revisao_km = db.Column(db.Integer, nullable=True)
    revisao_periodo = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_peca": self.nome_peca,
            "intervalo_km": self.intervalo_km,
            "intervalo_periodo": self.intervalo_periodo,
            "historico_km": self.historico_km,
            "historico_periodo": self.historico_periodo,
            "revisao_km": self.revisao_km,
            "revisao_periodo": self.revisao_periodo
        }