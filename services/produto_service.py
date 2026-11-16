from models.models import Produto, Pedido, ItemPedido, db


def listar_produtos(busca: str = "", categoria: str = "") -> list[Produto]:
    q = db.session.query(Produto)
    if busca:
        q = q.filter(Produto.nome.ilike(f"%{busca}%"))
    if categoria:
        q = q.filter(Produto.categoria == categoria)
    return q.order_by(Produto.nome).all()


def listar_categorias() -> list[str]:
    linhas = db.session.query(Produto.categoria).distinct().all()
    return sorted(c[0] for c in linhas if c[0])


def get_produto(produto_id: int) -> Produto:
    return db.session.get(Produto, produto_id)


def _validar(nome, preco, estoque):
    if not nome or preco in (None, "") or estoque in (None, ""):
        raise ValueError("Preencha nome, preço e estoque.")
    try:
        preco = float(str(preco).replace(",", "."))
        estoque = int(estoque)
    except ValueError:
        raise ValueError("Preço ou estoque inválido.")
    if preco < 0 or estoque < 0:
        raise ValueError("Preço e estoque não podem ser negativos.")
    return preco, estoque


def criar_produto(nome, descricao, preco, estoque, imagem_url, categoria) -> Produto:
    preco, estoque = _validar(nome, preco, estoque)
    p = Produto(nome=nome, descricao=descricao, preco=preco, estoque=estoque,
                imagem_url=imagem_url, categoria=categoria)
    db.session.add(p)
    db.session.commit()
    return p


def atualizar_produto(produto_id, nome, descricao, preco, estoque, imagem_url, categoria) -> Produto:
    p = get_produto(produto_id)
    if not p:
        raise ValueError("Produto não encontrado.")
    preco, estoque = _validar(nome, preco, estoque)
    p.nome, p.descricao, p.preco = nome, descricao, preco
    p.estoque, p.imagem_url, p.categoria = estoque, imagem_url, categoria
    db.session.commit()
    return p


def excluir_produto(produto_id) -> None:
    p = get_produto(produto_id)
    if not p:
        raise ValueError("Produto não encontrado.")
    db.session.delete(p)
    db.session.commit()


def montar_carrinho(carrinho: dict):
    """carrinho = {"id_produto": quantidade}. Retorna (linhas, total)."""
    linhas, total = [], 0.0
    for pid, qtd in carrinho.items():
        p = get_produto(int(pid))
        if not p:
            continue
        subtotal = p.preco * qtd
        total += subtotal
        linhas.append({"produto": p, "quantidade": qtd, "subtotal": subtotal})
    return linhas, total


def finalizar_pedido(usuario_id: int, carrinho: dict) -> Pedido:
    linhas, total = montar_carrinho(carrinho)
    if not linhas:
        raise ValueError("Seu carrinho está vazio.")
    for l in linhas:
        if l["quantidade"] > l["produto"].estoque:
            raise ValueError(f"Estoque insuficiente para {l['produto'].nome}.")

    pedido = Pedido(usuario_id=usuario_id, total=total)
    for l in linhas:
        p = l["produto"]
        p.estoque -= l["quantidade"]
        pedido.itens.append(ItemPedido(produto_id=p.id, nome_produto=p.nome,
                                       preco_unitario=p.preco, quantidade=l["quantidade"]))
    db.session.add(pedido)
    db.session.commit()
    return pedido


def pedidos_do_usuario(usuario_id: int) -> list[Pedido]:
    return (db.session.query(Pedido).filter_by(usuario_id=usuario_id)
            .order_by(Pedido.criado_em.desc()).all())
