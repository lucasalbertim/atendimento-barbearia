from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from . import db  # Importação relativa
from .models import Cliente, Visita, Servico, Pagamento

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

@bp.route('/servicos')
def list_servicos():
    servicos = Servico.query.all()
    return render_template('list_servicos.html', servicos=servicos)

@bp.route('/add_pagamento', methods=['POST'])
def add_pagamento():
    visita_id = request.form['visita_id']
    forma = request.form['forma']
    pagamento = Pagamento(visita_id=visita_id, forma=forma)
    db.session.add(pagamento)
    db.session.commit()
    return redirect(url_for('main.list_pagamentos'))

@bp.route('/pagamentos')
def list_pagamentos():
    pagamentos = Pagamento.query.all()
    return render_template('list_pagamentos.html', pagamentos=pagamentos)

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

@bp.route('/cliente/<int:cliente_id>')
def cliente_visitas(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    total_visitas = Visita.query.filter_by(cliente_id=cliente.id).count()
    return render_template('cliente_visitas.html', cliente=cliente, total_visitas=total_visitas)

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

@bp.route('/projecao_ganhos')
def projecao_ganhos():
    # Calcular soma dos valores dos serviços realizados
    visitas = Visita.query.all()
    total_ganho = sum(Servico.query.get(visita.servico_id).preco for visita in visitas)

    # Calcular total de visitas
    total_visitas = len(visitas)

    # Se não houver visitas, retorne 0 para a projeção
    if total_visitas == 0:
        return render_template('projecao_ganhos.html', total_ganho=total_ganho, projecao_mensal=0)

    # Calcular a data mais antiga de visita
    data_mais_antiga = min(visita.data for visita in visitas)
    dias_decorridos = (datetime.now() - data_mais_antiga).days or 1  # Evitar divisão por zero

    # Média de visitas por dia
    media_visitas = total_visitas / dias_decorridos

    # Obter todos os serviços para calcular a projeção
    servicos = Servico.query.all()
    preco_servico = sum(servico.preco for servico in servicos) / max(1, len(servicos)) if servicos else 0

    # Projeção para 30 dias
    projecao_mensal = media_visitas * 30 * preco_servico

    return render_template('projecao_ganhos.html', total_ganho=total_ganho, projecao_mensal=projecao_mensal)
