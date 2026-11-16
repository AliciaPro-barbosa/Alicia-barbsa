from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from services.produto_service import (
    listar_produtos, listar_categorias, get_produto, criar_produto, atualizar_produto,
    excluir_produto, montar_carrinho, finalizar_pedido, pedidos_do_usuario)
from .auth_decorator import login_required

loja_bp = Blueprint('loja', __name__, url_prefix='/loja', template_folder='templates')


# ---------- Vitrine (pública) ----------
@loja_bp.route('/')
def vitrine():
    busca = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()
    return render_template('loja.html', produtos=listar_produtos(busca, categoria),
                           categorias=listar_categorias(), busca=busca, categoria=categoria)


@loja_bp.route('/produto/<int:produto_id>')
def detalhe(produto_id):
    produto = get_produto(produto_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for('loja.vitrine'))
    return render_template('produto.html', produto=produto)


# ---------- Carrinho (guardado na session) ----------
@loja_bp.route('/carrinho')
def carrinho():
    linhas, total = montar_carrinho(session.get('carrinho', {}))
    return render_template('carrinho.html', linhas=linhas, total=total)


@loja_bp.route('/carrinho/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    produto = get_produto(produto_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for('loja.vitrine'))

    try:
        qtd = max(1, int(request.form.get('quantidade', 1)))
    except ValueError:
        qtd = 1

    carrinho = session.get('carrinho', {})
    chave = str(produto_id)
    nova_qtd = carrinho.get(chave, 0) + qtd
    if nova_qtd > produto.estoque:
        flash(f"Só temos {produto.estoque} unidade(s) de {produto.nome}.", "warning")
        return redirect(url_for('loja.detalhe', produto_id=produto_id))

    carrinho[chave] = nova_qtd
    session['carrinho'] = carrinho
    flash(f"{produto.nome} adicionado ao carrinho.", "success")
    return redirect(url_for('loja.carrinho'))


@loja_bp.route('/carrinho/remover/<int:produto_id>', methods=['POST'])
def remover_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    carrinho.pop(str(produto_id), None)
    session['carrinho'] = carrinho
    return redirect(url_for('loja.carrinho'))


@loja_bp.route('/carrinho/finalizar', methods=['POST'])
@login_required
def finalizar():
    try:
        pedido = finalizar_pedido(session['user_id'], session.get('carrinho', {}))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('loja.carrinho'))
    session['carrinho'] = {}
    flash(f"Pedido #{pedido.id} realizado com sucesso!", "success")
    return redirect(url_for('loja.meus_pedidos'))


@loja_bp.route('/pedidos')
@login_required
def meus_pedidos():
    return render_template('pedidos.html', pedidos=pedidos_do_usuario(session['user_id']))


# ---------- Administração de produtos (exige login) ----------
@loja_bp.route('/admin')
@login_required
def admin_produtos():
    return render_template('admin_produtos.html', produtos=listar_produtos())


def _dados_form():
    f = request.form
    return (f.get('nome', '').strip(), f.get('descricao', '').strip(), f.get('preco'),
            f.get('estoque'), f.get('imagem_url', '').strip(), f.get('categoria', '').strip())


@loja_bp.route('/admin/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        try:
            criar_produto(*_dados_form())
            flash("Produto cadastrado!", "success")
            return redirect(url_for('loja.admin_produtos'))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template('produto_form.html', produto=None)


@loja_bp.route('/admin/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = get_produto(produto_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for('loja.admin_produtos'))
    if request.method == 'POST':
        try:
            atualizar_produto(produto_id, *_dados_form())
            flash("Produto atualizado!", "success")
            return redirect(url_for('loja.admin_produtos'))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template('produto_form.html', produto=produto)


@loja_bp.route('/admin/excluir/<int:produto_id>', methods=['POST'])
@login_required
def excluir(produto_id):
    try:
        excluir_produto(produto_id)
        flash("Produto excluído.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('loja.admin_produtos'))
