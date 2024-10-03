from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL', 'postgresql://postgres:password@localhost/barbearia_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definição do modelo Cliente (exemplo)
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de cadastro de clientes
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        
        novo_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()
        
        return redirect(url_for('clientes'))
    
    return render_template('clientes.html')

# Rota para a página de serviços
@app.route('/servicos', methods=['GET', 'POST'])
def servicos():
    if request.method == 'POST':
        # Aqui você deve adicionar a lógica para lidar com os serviços
        # Exemplo: Capturar serviços selecionados e pagamento
        return redirect(url_for('servicos'))
    
    return render_template('servicos.html')

# Rota para a página de relatórios
@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
