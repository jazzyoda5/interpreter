from flask import (
    Blueprint,
    render_template
)


pg = Blueprint('playground', __name__)


@pg.route('/')
def index():
    return render_template('pg/index.html')