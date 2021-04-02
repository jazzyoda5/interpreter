#######################################
#######################################
# AST NODES
#######################################
#######################################

class AST(object):
    pass


class Block(AST):
    def __init__(self):
        self.children = []


class Number(AST):
    def __init__(self, token):
        self.value = token.value
        self.token = token


class Boolean(AST):
    def __init__(self, token):
        self.value = token.value
        self.token = token


class String(AST):
    def __init__(self, token):
        self.value = token.value
        self.token = token


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.token = self.op


class Comparison(AST):
    def __init__(self, left, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right
        self.token = self.op


# Example -> b: int = -a; <- Unary operation
class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Assign(AST):
    def __init__(self, name, value, type=None):
        self.name = name
        self.type = type
        self.value = value


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Value(AST):
    # Something that has only a value
    # Like a boolean or a string
    def __init__(self, value):
        self.value = value


class Print(AST):
    def __init__(self):
        self.args = []


class IfStatement(AST):
    def __init__(self, value, block, elseblock=None):
        self.value = value
        self.block = block
        self.elseblock = elseblock


class Param(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class FuncDecl(AST):
    def __init__(self, func_name, params, block_node, returns=None):
        self.func_name = func_name
        self.params = params # This is a list of parameter nodes
        self.block_node = block_node
        self.returns = returns


class FuncCall(AST):
    def __init__(self, func_name, params, token):
        self.func_name = func_name
        self.params = params
        self.token = token
class Empty(AST):
    pass
