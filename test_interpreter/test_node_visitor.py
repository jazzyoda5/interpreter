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
