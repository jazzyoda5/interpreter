import pytest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.semantic_analyser import SemanticAnalyzer
from interpreter.interpreter import Interpreter


@pytest.fixture
def tree(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    sem_an = SemanticAnalyzer(tree)
    sem_an.analyse()
    return tree


@pytest.mark.parametrize(
    'text', [("""
        a: int = 12;
        print(a);
    """)]
)    
def test_int_1(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == '12\n'

@pytest.mark.parametrize(
    'text', [("""
        a: int = 12;
        print('a is ', a);
    """)]
)    
def test_int_2(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == 'a is 12\n'

@pytest.mark.parametrize(
    'text', [("""
        a: str = '12';
        print('a is ', a);
    """)]
)    
def test_int_3(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == 'a is 12\n'

@pytest.mark.parametrize(
    'text', [("""
        function some_function(a: int) {
            b: int = a + 1;
            return (b);
        }    
        print(some_function(2));
    """)]
)    
def test_int_3(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == '3\n'

@pytest.mark.parametrize(
    'text', [("""
        function factorial(a: int) {
            if (a == 1) {
                return(1);
            } else {
                return(a * factorial(a - 1));
            }
        }    
        print('Factorial of 3 is : ', factorial(4));
    """)]
)    
def test_int_4(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == 'Factorial of 3 is : 24\n'

@pytest.mark.parametrize(
    'text', [("""
        return(3); 
    """)]
)    
def test_int_5(tree, capsys):
    interpreter = Interpreter(tree)
    with pytest.raises(Exception) as excinfo:
        result = interpreter.interpret()
    assert 'Invalid syntax' in str(excinfo)

@pytest.mark.parametrize(
    'text', [("""
        some_int: int = 45;
        if (some_int == 45) {
            print('it is indeed 45');
        } else {
            print('it is not 45');
        }
    """)]
)    
def test_int_6(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == 'it is indeed 45\n'

@pytest.mark.parametrize(
    'text', [("""
        a: str = 'I am ';
        b: str = 'Jakob';
        print(a + b); 
    """)]
)    
def test_int_7(tree, capsys):
    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    assert result == 'success'
    captured = capsys.readouterr()
    assert captured.out == 'I am Jakob\n'

@pytest.mark.parametrize(
    'text', [("""
        a: str = 'I am ';
        b: int = 12;
        c: int = a + b; 
    """)]
)    
def test_int_7(tree, capsys):
    interpreter = Interpreter(tree)
    with pytest.raises(Exception) as excinfo:
        result = interpreter.interpret()

    assert 'Error: Can not run + operation on types str and int' in str(excinfo)
    


    





