from flask import (
    Blueprint,
    render_template,
    request,
    session,
    jsonify
)
import json
from io import StringIO 
import sys
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.semantic_analyser import SemanticAnalyzer
from interpreter.interpreter import Interpreter


pg = Blueprint('playground', __name__)


@pg.route('/')
def index():
    return render_template('pg/index.html')


@pg.route('/about')
def about():
    return render_template('pg/docs.html')

# Api


def run_interpreter(text):
    result = {}
    result['output'] = []
    with Capturing() as output:
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            tree = parser.parse()
            sem_an = SemanticAnalyzer(tree)
            sem_an.analyse()
            interpreter = Interpreter(tree)
            result['final_result'] = interpreter.interpret()
        except Exception as exc:
            result['exception'] = str(exc)

    if output:
        result['output'] = output

    return result


class Capturing(list): # Context manager that catches stdout output
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


@pg.route('/api/runcode', methods=['POST'])
def run_code():
    request_data = json.loads(request.data)
    text = request_data['code']
    # Interpreter the code
    result = run_interpreter(text)

    response = {
        'success': 'success',
        'int_result': result
    }
    return jsonify(response)