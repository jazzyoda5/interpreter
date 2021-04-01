from .ast import ( 
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

#######################################
#######################################
# PARSER
#######################################
#######################################


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()

    def error(self):
        raise Exception('ParserError: Invalid syntax')

    def eat(self, token_type):
        # Check if curr_token's type matches the passed in type
        if self.curr_token.type == token_type:
            self.curr_token = self.lexer.get_next_token()
        else:
            print('token on error: ', self.curr_token)
            self.error()

    def parse(self):
        node = self.block()
        return node

    # Parent node of each program but also inner scoped blocks
    def block(self):
        """ block  :  compound_statement """
        return self.compound_statement()

    def compound_statement(self):
        """ compound_statement  :  statement_list """
        nodes = self.statement_list()
        root = Block()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """ statement_list  :  statement SCOLON
                            | statement 
                            | statement SCOLON statement_list """
        statements = []
        while True:
            statement = self.statement()
            statements.append(statement)
            if isinstance(statement, IfStatement) or isinstance(statement, FuncDecl):
                pass
            elif self.curr_token.type != 'SCOLON':
                break
            else:
                self.eat('SCOLON')

        return statements

    def statement(self):
        """ statement  =  block
                          | assignment
                          | function_declaration
                          | empty """

        token = self.curr_token
        print(token)
        if token.type == 'NAME':  # Could be function call(?)
            node = self.assignment()

        elif token.type == 'PRINT':
            node = self.print()
            
        elif token.type == 'IF':
            node = self.ifelse()

        elif token.type == 'FUNCDECL':
            node = self.functiondecl()
        else:
            node = self.empty()
        
        return node

    #######################################
    # Arithmetic expressions 
    #######################################
    
    def factor(self):
        token = self.curr_token
        if token.type == 'PLUS':
            op = token
            self.eat('PLUS')
            node = UnaryOp(op=token, expr=self.factor())

        elif token.type == 'MINUS':
            op = token
            self.eat('MINUS')
            node = UnaryOp(op=token, expr=self.factor())
        
        elif token.type == 'INTEGER':
            node = Number(token=token)
            self.eat('INTEGER')

        elif token.type == 'FLOAT':
            node = Float(token=token)
            self.eat('FLOAT')

        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')

        elif token.type == 'NAME':
            node = self.variable()
        else:
            self.error()
        
        return node
        
    def term(self):
        """ term   : factor ((MUL | DIV) factor)* """
        node = self.factor()
        
        while self.curr_token.type in ('MULT', 'DIV'):
            token = self.curr_token
            if token.type == 'MULT':
                self.eat('MULT')
            elif token.type == 'DIV':
                self.eat('DIV')
            node = BinOp(left=node, op=token, right=self.factor())
        
        return node            

    def expr(self):
        """ expr   : term ((PLUS | MINUS) term)* """
        node = self.term()

        while self.curr_token.type in ('PLUS', 'MINUS'):
            token = self.curr_token
            if token.type == 'PLUS': 
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')
            node = BinOp(left=node, op=token, right=self.term())

        return node

    #######################################
    # IF ELSE  
    #######################################

    def ifelse(self):
        """ ifelse  :  IF comparison LBRACE block RBRACE (ELSE LBRACE block RBRACE) """        
        self.eat('IF')
        comparison = self.comparison()
        self.eat('LBRACE')
        block = self.block()
        self.eat('RBRACE')
        node = IfStatement(value=comparison, block=block)
 
        if self.curr_token.type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            elseblock = self.block()
            self.eat('RBRACE')
            node.elseblock = elseblock
        
        return node 

    def comparison(self):
        """ comparison  :  LPAREN variable 
                                  | VALUE 
                                  | (variable | expr) op (variable | expr)
                           RPAREN """
        self.eat('LPAREN')
        
        if self.curr_token.type == 'BOOL':
            left = Boolean(token=self.curr_token)
            self.eat('BOOL')
        else:
            left = self.expr()
        
        if self.curr_token.type == 'RPAREN':
            self.eat('RPAREN')
            print('jakob234')
            return Comparison(left=left)
        
        # Check for comparison operator
        token = self.curr_token
        if token.type == 'GRTHAN':
            op = token
            self.eat('GRTHAN')
        elif token.type == 'LSTHAN':
            op = token
            self.eat('LSTHAN')
        elif token.type == 'ISEQUAL':
            op = token
            self.eat('ISEQUAL')
        elif token.type == 'LSTHEQ':
            op = token
            self.eat('LSTHEQ')
        elif token.type == 'GRTHEQ':
            op = token
            self.eat('GRTHEQ')
        else:
            print('token at comparison error: ', token)
            self.error()

        # Right side of comparison
        if self.curr_token.type == 'BOOL':
            right = Boolean(token=self.curr_token)
        else:
            right = self.expr()
        
        self.eat('RPAREN')
        return Comparison(left=left, op=op, right=right)

    def variable(self):
        token = self.curr_token
        self.eat('NAME')
        return Var(token=token)
    
    def print(self):
        """ PRINT  LPAREN (expr | STRING | BOOL (COMMA))* RPAREN """
        self.eat('PRINT')
        self.eat('LPAREN')
        
        node = Print() # So Print can take multiple args

        while True:
            token = self.curr_token
            print('token at print: ', token)
            if token.type == 'STRING':
                node.args.append(String(token=token))
                self.eat('STRING')
            elif token.type == 'BOOL':
                node.args.append(Boolean(token=token))
                self.eat('BOOL')
            else:
                node.args.append(self.expr()) # Arithmetic expression

            if self.curr_token.type == 'COMMA':
                self.eat('COMMA')
            else:
                break

        self.eat('RPAREN')
        return node
        
    def assignment(self):
        """ variable COLON TYPE EQUAL expr 
                                      | variable """
        name = self.variable()
        self.eat('COLON')
        var_type = self.curr_token
        self.eat('TYPE')
        self.eat('EQUAL')
        
        if self.curr_token.type == 'STRING':
            value = String(token=self.curr_token)

        elif self.curr_token.type == 'BOOL':
            value = Boolean(token=self.curr_token)
        else:
            value = self.expr()

        node = Assign(name=name, type=var_type, value=value)
        return node                

    def empty(self):
        return Empty()
