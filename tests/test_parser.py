import pytest
from interpreter.ast import (
    Float,
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
    Empty
)
from interpreter.lexer import Lexer, Token
from interpreter.parser import Parser

##################################
##################################
# PARSER TESTS
##################################
##################################


def test_parser_print_str():
    text = 'print("Hello");'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    # First node should be Block
    assert isinstance(node1, Block)
    assert len(node1.children) == 2 # Print node and Empty node

    node2 = node1.children[0]
    assert isinstance(node2, Print)
    assert len(node2.args) == 1

    node3 = node2.args[0]
    assert isinstance(node3, String)
    assert node3.value == 'Hello'


def test_parser_print_bool():
    text = 'print(True);'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    # First node should be Block
    assert isinstance(node1, Block)
    assert len(node1.children) == 2 # Print node and Empty node

    node2 = node1.children[0]
    assert isinstance(node2, Print)
    assert len(node2.args) == 1

    node3 = node2.args[0]
    assert isinstance(node3, Boolean)
    assert node3.value == True


def test_parser_print_multargs():
    text = 'print(True, "str");'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    # First node should be Block
    assert isinstance(node1, Block)
    assert len(node1.children) == 2 # Print node and Empty node

    node2 = node1.children[0]
    assert isinstance(node2, Print)
    assert len(node2.args) == 2

    node3 = node2.args[0]
    assert isinstance(node3, Boolean)
    assert node3.value == True

    node4 = node2.args[1]
    assert isinstance(node4, String)
    assert node4.value == "str"


def test_parser_int_assign():
    text = 'a: int = 46;'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    assert isinstance(node1, Block)
    assert len(node1.children) == 2 

    node2 = node1.children[0]
    assert isinstance(node2, Assign)
    assert isinstance(node2.name, Var)
    assert node2.type.type == 'TYPE' # TYPE Token as type
    assert node2.type.value == 'int'
    assert isinstance(node2.value, Number)
    
    node3 = node2.value
    assert node3.value == 46

def test_parser_expr_assign():
    text = 'a: int = (12 + 2) * 2;'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    assert isinstance(node1, Block)
    assert len(node1.children) == 2 

    node2 = node1.children[0]
    assert isinstance(node2, Assign)
    assert isinstance(node2.name, Var)
    assert node2.type.type == 'TYPE' # TYPE Token as type
    assert node2.type.value == 'int'
    assert isinstance(node2.value, BinOp)

    node3 = node2.value
    assert isinstance(node3.left, BinOp)
    assert node3.op.value == '*'
    assert isinstance(node3.right, Number) 

    node4 = node3.left
    assert isinstance(node4.left, Number)
    assert node4.op.value == '+'
    assert isinstance(node4.right, Number)
   
def test_parser_str_assign():
    text = 'a: str = "string";'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    assert isinstance(node1, Block)
    assert len(node1.children) == 1 

    node2 = node1.children[0]
    assert isinstance(node2, Assign)
    assert isinstance(node2.name, Var)
    assert node2.type.type == 'TYPE' # TYPE Token as type
    assert node2.type.value == 'str'
    assert isinstance(node2.value, String)
    
    node3 = node2.value
    assert node3.value == 'string'

def test_parser_bool_assign():
    text = 'variable: bool = True;'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    assert isinstance(node1, Block)
    assert len(node1.children) == 1 

    node2 = node1.children[0]
    assert isinstance(node2, Assign)
    assert isinstance(node2.name, Var)
    assert node2.type.type == 'TYPE' # TYPE Token as type
    assert node2.type.value == 'bool'
    assert isinstance(node2.value, Boolean)
    
    node3 = node2.value
    assert node3.value == True

def test_parser_float_assign():
    text = 'variable: float = 1.2;'
    lexer = Lexer(text)
    parser = Parser(lexer)
    node1 = parser.parse()

    assert isinstance(node1, Block)
    assert len(node1.children) == 2 

    node2 = node1.children[0]
    assert isinstance(node2, Assign)
    assert isinstance(node2.name, Var)
    assert node2.type.type == 'TYPE' # TYPE Token as type
    assert node2.type.value == 'float'
    assert isinstance(node2.value, Float)
    
    node3 = node2.value
    assert node3.value == 1.2

def test_parser_if_true():
    text = """
        if (True) {
            print('yo');
        } """
    lexer = Lexer(text)
    parser = Parser(lexer)
    block = parser.parse()
    if_node = block.children[0]
    assert isinstance(if_node, IfStatement)


    assert isinstance(if_node.value, Comparison)
    comparison = if_node.value
    assert comparison.left.value == True
    assert comparison.op is None
    assert comparison.right is None

    assert isinstance(if_node.block, Block)
    assert if_node.elseblock is None

    block_node = if_node.block
    assert isinstance(block_node.children[0], Print)

def test_parser_if_comparison():
    text = """
        if (a > 2) {
            print('yo');
        } """
    lexer = Lexer(text)
    parser = Parser(lexer)
    block = parser.parse()
    if_node = block.children[0]
    assert isinstance(if_node, IfStatement)

    assert isinstance(if_node.value, Comparison)
    assert isinstance(if_node.block, Block)
    assert if_node.elseblock is None

    comp_node = if_node.value
    assert isinstance(comp_node.left, Var)
    assert comp_node.op.value == '>'
    assert isinstance(comp_node.right, Number)


           
