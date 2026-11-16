from flask import Blueprint, render_template
from services.produto_service import listar_produtos

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
    destaques = listar_produtos()[:4]
    return render_template('index.html', destaques=destaques)
