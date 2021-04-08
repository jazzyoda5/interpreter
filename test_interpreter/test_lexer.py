from interpreter.lexer import Lexer, Token

#######################################
#######################################
# LEXER TESTS
#######################################
#######################################

def test_lexer_symbols():
    # Test with so many asserts probably not the 
    # best idea, might change this
    text = '+ = ; : () == <= >='
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'PLUS'
    assert next_token.value == '+'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EQUAL'
    assert next_token.value == '='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'COLON'
    assert next_token.value == ':'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'ISEQUAL'
    assert next_token.value == '=='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SMTHEQ'
    assert next_token.value == '<='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'GRTHEQ'
    assert next_token.value == '>='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_integers1():
    text = '4'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'INTEGER'
    assert next_token.value == 4

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_integers2():
    text = '87'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'INTEGER'
    assert next_token.value == 87

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_integers3():
    text = '23498'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'INTEGER'
    assert next_token.value == 23498

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_builtin_names_type():
    reserved_names = {
        'str': 'TYPE',
        'int': 'TYPE',
        'bool': 'TYPE',
        'float': 'TYPE'
    }

    for key, val in reserved_names.items():
        lexer = Lexer(key)

        next_token = lexer.get_next_token()
        assert next_token is not None
        assert isinstance(next_token, Token)
        assert next_token.type == val
        assert next_token.value == key


def test_lexer_var_names():
    var_names = [
        'a',
        'Yo',
        'variable',
        'some_var',
        'WhatEver'
    ]
    for name in var_names:
        lexer = Lexer(name)

        next_token = lexer.get_next_token()
        assert next_token is not None
        assert isinstance(next_token, Token)
        assert next_token.type == 'NAME'
        assert next_token.value == name


def test_lexer_int_decl():
    text = 'var: int = 45;'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'var'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'COLON'
    assert next_token.value == ':'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'TYPE'
    assert next_token.value == 'int'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EQUAL'
    assert next_token.value == '='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'INTEGER'
    assert next_token.value == 45

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_str_decl():
    text = 'var: str = "I am s string";'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'var'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'COLON'
    assert next_token.value == ':'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'TYPE'
    assert next_token.value == 'str'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EQUAL'
    assert next_token.value == '='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'STRING'
    assert next_token.value == 'I am s string'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_float_decl():
    text = 'var: float = 1.56;'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'var'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'COLON'
    assert next_token.value == ':'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'TYPE'
    assert next_token.value == 'float'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EQUAL'
    assert next_token.value == '='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'FLOAT'
    assert next_token.value == 1.56

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_bool_decl():
    text = 'var: bool = True;'
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'var'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'COLON'
    assert next_token.value == ':'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'TYPE'
    assert next_token.value == 'bool'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EQUAL'
    assert next_token.value == '='

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'BOOL'
    assert next_token.value == True

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


#######################################
# Function declaration
#######################################

def test_lexer_langdecl1():
    text = """
        function some_function() {
            print('Hello');
            return();
        }
    """
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'FUNCDECL'
    assert next_token.value == 'function'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'some_function'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LBRACE'
    assert next_token.value == '{'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'PRINT'
    assert next_token.value == 'print'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'STRING'
    assert next_token.value == 'Hello'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RETURN'
    assert next_token.value == 'return'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RBRACE'
    assert next_token.value == '}'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None

#########################################
# If Else
#########################################

def test_lexer_langdecl1():
    text = """
        if (a > 68) {
            print(a);
        } else {
            print(68);
        }
    """
    lexer = Lexer(text)

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'IF'
    assert next_token.value == 'if'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'a'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'GRTHAN'
    assert next_token.value == '>'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'INTEGER'
    assert next_token.value == 68

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LBRACE'
    assert next_token.value == '{'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'PRINT'
    assert next_token.value == 'print'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'NAME'
    assert next_token.value == 'a'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RBRACE'
    assert next_token.value == '}'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'ELSE'
    assert next_token.value == 'else'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LBRACE'
    assert next_token.value == '{'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'PRINT'
    assert next_token.value == 'print'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'LPAREN'
    assert next_token.value == '('

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'INTEGER'
    assert next_token.value == 68

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RPAREN'
    assert next_token.value == ')'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'SCOLON'
    assert next_token.value == ';'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'RBRACE'
    assert next_token.value == '}'

    next_token = lexer.get_next_token()
    assert next_token is not None
    assert isinstance(next_token, Token)
    assert next_token.type == 'EOF'
    assert next_token.value == None


def test_lexer_comments():
    text = """
        /*
        I am a comment
        */
        a: int = 1;
    """
    lexer = Lexer(text)

    token = lexer.get_next_token()
    assert isinstance(token, Token)
    assert token.type == 'NAME'
    assert token.value == 'a'