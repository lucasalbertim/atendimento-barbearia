from app import db
from datetime import datetime

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    visitas = db.relationship('Visita', backref='cliente', lazy=True)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tempo_estimado = db.Column(db.Integer, nullable=False)  # em minutos

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forma = db.Column(db.String(20), nullable=False)
    visita_id = db.Column(db.Integer, db.ForeignKey('visita.id'), nullable=False)

# app/models.py

class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    tempo_estimado = db.Column(db.Integer)  # Tempo de espera calculado
    pagamento = db.relationship('Pagamento', backref='visita', lazy=True)

