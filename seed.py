"""Popula o banco com produtos de exemplo. Rode: python seed.py"""
from app import app
from models.models import Produto, db

EXEMPLOS = [
    ("Camiseta Básica", "Camiseta 100% algodão, confortável para o dia a dia.", 49.90, 25, "Roupas"),
    ("Tênis Esportivo", "Tênis leve para corrida e caminhada.", 229.90, 10, "Calçados"),
    ("Mochila Urbana", "Mochila resistente com compartimento para notebook.", 159.90, 15, "Acessórios"),
    ("Fone Bluetooth", "Fone sem fio com bateria de até 20 horas.", 119.90, 30, "Eletrônicos"),
    ("Garrafa Térmica", "Mantém a temperatura por 12 horas. 500 ml.", 59.90, 40, "Acessórios"),
    ("Relógio Digital", "Relógio resistente à água com cronômetro.", 139.90, 8, "Acessórios"),
    ("Calça Jeans", "Corte reto, tecido com elastano.", 119.90, 20, "Roupas"),
    ("Smartwatch", "Monitor de batimentos, passos e notificações.", 299.90, 5, "Eletrônicos"),
]

with app.app_context():
    if Produto.query.count() == 0:
        for nome, desc, preco, estoque, cat in EXEMPLOS:
            db.session.add(Produto(nome=nome, descricao=desc, preco=preco, estoque=estoque, categoria=cat))
        db.session.commit()
        print(f"{len(EXEMPLOS)} produtos criados.")
    else:
        print("Já existem produtos; nada a fazer.")
