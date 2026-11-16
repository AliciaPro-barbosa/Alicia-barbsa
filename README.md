# Minha Loja

Projeto de loja virtual desenvolvido com Python e Flask, utilizando SQLAlchemy e SQLite.

## Tecnologias
- Python
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- HTML (templates Jinja2)

## Como executar localmente

1. Entre na pasta do projeto.
2. Crie e ative um ambiente virtual (opcional, mas recomendado).
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. (Opcional) Cadastre produtos de exemplo:

```bash
python seed.py
```

5. Inicie a aplicação:

```bash
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador.

## Funcionalidades
- Página inicial e vitrine de produtos
- Busca e filtro por categoria
- Página de detalhes do produto
- Carrinho de compras
- Finalização de pedidos e atualização de estoque
- Cadastro e login de usuários
- Histórico de pedidos
- Área administrativa para gerenciamento de produtos

## Estrutura
- `app.py`: inicialização da aplicação Flask
- `models/`: modelos e configuração do banco de dados
- `routes/`: rotas da aplicação
- `services/`: regras de negócio
- `templates/`: páginas HTML

Este repositório contém o código-fonte do projeto acadêmico.
