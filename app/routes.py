from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from datetime import datetime
from app.models import Cliente, Visita, Servico, Pagamento

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

@bp.route('/add_cliente', methods=['GET', 'POST'])
def add_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        novo_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_cliente.html')

# Rota para adicionar serviços
@bp.route('/add_servico', methods=['GET', 'POST'])
def add_servico():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        tempo_estimado = int(request.form['tempo_estimado'])
        novo_servico = Servico(nome=nome, preco=preco, tempo_estimado=tempo_estimado)
        db.session.add(novo_servico)
        db.session.commit()
        return redirect(url_for('main.list_servicos'))
    return render_template('add_servico.html')

# Rota para listar serviços
@bp.route('/servicos')
def list_servicos():
    servicos = Servico.query.all()
    return render_template('list_servicos.html', servicos=servicos)

# Rota para registrar pagamento
@bp.route('/add_pagamento', methods=['POST'])
def add_pagamento():
    visita_id = request.form['visita_id']
    forma = request.form['forma']
    pagamento = Pagamento(visita_id=visita_id, forma=forma)
    db.session.add(pagamento)
    db.session.commit()
    return redirect(url_for('main.list_pagamentos'))

# Rota para listar pagamentos
@bp.route('/pagamentos')
def list_pagamentos():
    pagamentos = Pagamento.query.all()
    return render_template('list_pagamentos.html', pagamentos=pagamentos)

# Rota para gerar relatório de visitas por período
@bp.route('/relatorio', methods=['GET', 'POST'])
def relatorio():
    if request.method == 'POST':
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        
        # Convertendo strings para formato de data
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

        visitas = Visita.query.filter(Visita.data.between(data_inicio, data_fim)).all()
        return render_template('relatorio.html', visitas=visitas)
    
    return render_template('relatorio_form.html')

# Rota para exibir as métricas de visita de um cliente
@bp.route('/cliente/<int:cliente_id>')
def cliente_visitas(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    total_visitas = Visita.query.filter_by(cliente_id=cliente.id).count()
    return render_template('cliente_visitas.html', cliente=cliente, total_visitas=total_visitas)

# Rota para adicionar uma visita e calcular tempo de espera
@bp.route('/add_visita', methods=['GET', 'POST'])
def add_visita():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        servico_id = request.form['servico_id']
        
        # Obter o serviço selecionado
        servico = Servico.query.get(servico_id)
        tempo_estimado = servico.tempo_estimado  # Tempo do serviço escolhido

        # Criar a visita
        nova_visita = Visita(cliente_id=cliente_id, servico_id=servico_id, tempo_estimado=tempo_estimado)
        db.session.add(nova_visita)
        db.session.commit()

        return redirect(url_for('main.list_visitas'))

    # Exibir lista de clientes e serviços no formulário
    clientes = Cliente.query.all()
    servicos = Servico.query.all()
    return render_template('add_visita.html', clientes=clientes, servicos=servicos)

# Rota para exibir projeção de ganhos futuros
@bp.route('/projecao_ganhos')
def projecao_ganhos():
    # Calcular soma dos valores dos serviços realizados
    visitas = Visita.query.all()
    total_ganho = 0
    for visita in visitas:
        servico = Servico.query.get(visita.servico_id)
        total_ganho += servico.preco

    # Projeção: se continuar na mesma média de visitas
    media_visitas = len(visitas) / max(1, (datetime.utcnow() - visitas[0].data).days)  # Média de visitas por dia
    projecao_mensal = media_visitas * 30 * servico.preco  # Projeção para 30 dias

    return render_template('projecao_ganhos.html', total_ganho=total_ganho, projecao_mensal=projecao_mensal)




