from interpreter.lexer import Lexer, Token
from interpreter.parser import Parser
from interpreter.ast import (
    Print,
    BinOp,
    Block,
    Number,
    String,
    Boolean,
    Comparison,
    Var,
    UnaryOp,
    Assign,
    IfStatement,
    Param,
    FuncDecl,
    FuncCall,
    Empty
)
from interpreter.semantic_analyser import (
    Symbol,
    SymbolTable,
    BuiltinTypeSymbol,
    FunctionSymbol,
    SemanticAnalyzer
)
from interpreter.interpreter import NodeVisitor
import pytest


@pytest.fixture
def tree(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    return tree

@pytest.mark.parametrize(
    'text', [('a: int = 12;')]  
)   
def test_sem_an_one_var(tree):
    analyser = SemanticAnalyzer(tree)
    result = analyser.analyse()
    assert result == 'success'


@pytest.mark.parametrize(
    'text', [('a: int = "string";')]  
)   
def test_sem_an_one_var(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception) as excinfo:
        result = analyser.analyse()

    assert 'not of type int' in str(excinfo)


@pytest.mark.parametrize(
    'text', [("""
        a: int = 12;
        print(a);
    """)]  
)   
def test_sem_an_one_var_print(tree):
    analyser = SemanticAnalyzer(tree)
    result = analyser.analyse()
    assert result == 'success'


@pytest.mark.parametrize(
    'text', [("""
        b: int = 12;
        print(a);
    """)]  
)   
def test_sem_an_var_doesnt_exist(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception):
        result = analyser.analyse()


text = """
    a: str = 'hey';
    if (a == 3) {
        print(b);
    }    
"""
@pytest.mark.parametrize(
    'text', [(text)]  
)   
def test_sem_an_if_block(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception) as excinfo:
        result = analyser.analyse()
    
    assert 'Symbol(identifier) not found' in str(excinfo.value)

@pytest.mark.parametrize(
    'text', [("""
        function yo_yo(a: int, b: str) {
            print(a, "Is a Number");
            print(b, "Is a String");
        }     
    """)]  
)   
def test_parser_correct_funcdecl(tree):
    analyser = SemanticAnalyzer(tree)
    result = analyser.analyse()
    assert result == 'success'

@pytest.mark.parametrize(
    'text', [("""
        function yo_yo(a: int, b: str) {
            print(a, "Is a Number");
            print(c, "Is a String");
        }     
    """)]  
)   
def test_parser_incorrect_funcdecl2(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception) as excinfo:
        result = analyser.analyse()
    
    assert 'Symbol(identifier) not found' in str(excinfo)



@pytest.mark.parametrize(
    'text', [("""
        a: int = 'heycy';
    """)]  
)   
def test_assign_wrong_type(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception) as excinfo:
        result = analyser.analyse()
    
    assert 'is not of type' in str(excinfo.value)

@pytest.mark.parametrize(
    'text', [("""
        function yo_yo(a: int, b: str) {
            print(a, "Is a Number");
            print(b, "Is a String");
        }
        yo_yo(4, 'yo');     
    """)]  
)   
def test_parser_correct_funccall(tree):
    analyser = SemanticAnalyzer(tree)
    result = analyser.analyse()
    assert result == 'success'

@pytest.mark.parametrize(
    'text', [( """
        function yo_yo(a: int, b: str) {
            print(a, "Is a Number");
            print(b, "Is a String");
        }
        yo_yo(4, 6);     
    """)]  
)   
def test_parser_invalid_funccall1(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception) as excinfo:
        result = analyser.analyse()
    
    assert "Error: Type of given arg doesn't match defined arg" in str(excinfo)

@pytest.mark.parametrize(
    'text', [( """
        function yo_yo(a: int, b: int) {
            print(a, "Is a Number");
            print(b, "Is a String");
        }
        yo_yo(4, 6, 89);     
    """)]  
)   
def test_sem_an_bad_funccall2(tree):
    analyser = SemanticAnalyzer(tree)
    with pytest.raises(Exception) as excinfo:
        result = analyser.analyse()
    
    assert "was expecting" in str(excinfo)


    