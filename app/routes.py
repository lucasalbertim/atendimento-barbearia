import calendar
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Cliente, Servico, Visita, Pagamento
from . import db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

# 1. Página inicial (Cliente realiza login via CPF ou Telefone)
@bp.route('/')
def index():
    return render_template('index.html')

# 2. Validação do CPF ou Telefone e redirecionamento para a escolha de serviços
@bp.route('/login_cliente', methods=['POST'])
def login_cliente():
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')

    cliente = None
    if cpf:
        cliente = Cliente.query.filter_by(cpf=cpf).first()
    elif telefone:
        cliente = Cliente.query.filter_by(telefone=telefone).first()

    if cliente:
        return redirect(url_for('main.escolher_servico', cliente_id=cliente.id))
    else:
        flash("CPF ou Telefone inválido.")
        return redirect(url_for('main.index'))

# 3. Tela de cadastro de novos clientes
@bp.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']

        # Verificar se CPF já existe no banco de dados
        cliente_existente = Cliente.query.filter_by(cpf=cpf).first()

        if cliente_existente:
            flash("Esse CPF já está cadastrado.")
            return redirect(url_for('main.cadastro_cliente'))

        # Adicionar novo cliente no banco
        novo_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('cadastro_cliente.html')

# 4. Escolher os serviços que o cliente deseja
@bp.route('/escolher_servico/<int:cliente_id>', methods=['GET', 'POST'])
def escolher_servico(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    servicos = Servico.query.all()

    if request.method == 'POST':
        servico_id = request.form['servico_id']

        # Buscar o serviço escolhido
        servico = Servico.query.get(servico_id)
        tempo_estimado = servico.tempo_estimado

        # Criar a visita para o cliente
        nova_visita = Visita(cliente_id=cliente.id, servico_id=servico.id, tempo_estimado=tempo_estimado)
        db.session.add(nova_visita)
        db.session.commit()

        flash("Serviço escolhido com sucesso!")
        return redirect(url_for('main.index'))

    return render_template('escolher_servico.html', cliente=cliente, servicos=servicos)

# 5. Gerenciar serviços (somente para administradores)
@bp.route('/admin/gerenciar_servicos', methods=['GET', 'POST'])
def gerenciar_servicos():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        tempo_estimado = int(request.form['tempo_estimado'])

        # Adicionar novo serviço no banco
        novo_servico = Servico(nome=nome, preco=preco, tempo_estimado=tempo_estimado)
        db.session.add(novo_servico)
        db.session.commit()

        flash("Serviço adicionado com sucesso!")
        return redirect(url_for('main.gerenciar_servicos'))

    servicos = Servico.query.all()
    return render_template('gerenciar_servicos.html', servicos=servicos)

# 6. Relatório de visitas (Administrador)
@bp.route('/admin/relatorio', methods=['GET', 'POST'])
def relatorio():
    if request.method == 'POST':
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']

        # Conversão para formato de data
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

        # Filtrar visitas por intervalo de data
        visitas = Visita.query.filter(Visita.data.between(data_inicio, data_fim)).all()

        return render_template('relatorio.html', visitas=visitas)

    return render_template('relatorio_form.html')

# 7. Métricas do painel do administrador
@bp.route('/admin/dashboard')
def admin_dashboard():
    total_clientes = Cliente.query.count()
    total_visitas = Visita.query.count()
    receita_total = db.session.query(func.sum(Servico.preco)).join(Visita, Servico.id == Visita.servico_id).scalar()
    
    # Média de visitas por cliente
    if total_clientes > 0:
        media_visitas_por_cliente = total_visitas / total_clientes
    else:
        media_visitas_por_cliente = 0

    # Métricas de retenção de clientes
    clientes_inativos = Cliente.query.outerjoin(Visita).filter(Visita.id == None).count()
    percentual_retentivo = ((total_clientes - clientes_inativos) / total_clientes * 100) if total_clientes > 0 else 0
    media_visitas_por_cliente = total_visitas / total_clientes if total_clientes > 0 else 0
    clientes_retorno = db.session.query(Cliente.id).join(Visita).group_by(Cliente.id).having(func.count(Visita.id) > 1).count()


    visitas_por_mes = db.session.query(
       func.extract('month', Visita.data).label('mes'),
       func.count(Visita.id).label('total_visitas')
    ).group_by('mes').all()

    labels = [calendar.month_name[int(mes)] for mes, _ in visitas_por_mes]
    data = [total_visitas for _, total_visitas in visitas_por_mes]

    clientes_inativos = db.session.query(Cliente).join(Visita).filter(
    Visita.data < (datetime.utcnow() - timedelta(days=30))
    ).count()   

    return render_template('admin_dashboard.html', total_clientes=total_clientes, total_visitas=total_visitas,
                           receita_total=receita_total, media_visitas_por_cliente=media_visitas_por_cliente,
                           percentual_retentivo=percentual_retentivo, labels=labels,  data=data, clientes_retorno=clientes_retorno
                           , clientes_inativos=clientes_inativos)

@bp.route('/admin/projecao_ganhos')
def projecao_ganhos():
    visitas = Visita.query.all()
    total_ganho = sum(Servico.query.get(visita.servico_id).preco for visita in visitas)

    # Lógica de projeção mensal
    if len(visitas) > 0:
        data_mais_antiga = min(visita.data for visita in visitas)
        dias_decorridos = (datetime.now() - data_mais_antiga).days or 1
        media_visitas = len(visitas) / dias_decorridos
        preco_medio_servico = sum(servico.preco for servico in Servico.query.all()) / len(Servico.query.all())
        projecao_mensal = media_visitas * 30 * preco_medio_servico
    else:
        projecao_mensal = 0

    return render_template('projecao_ganhos.html', total_ganho=total_ganho, projecao_mensal=projecao_mensal)
