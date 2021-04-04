from semantic_analyser import (
    BuiltinTypeSymbol,
    VarSymbol,
    FunctionSymbol,
    SymbolTable,
    Symbol
)
from enum import Enum

################################
# NODE VISITOR
################################


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


################################
# Call Stack
################################


class CallStack(object):
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        self.items.pop()
    
    def peek(self):
        return self.items[-1] # See what is at the top of the stack


class ActivationRecord:
    def __init__(self, name, type, scope_level):
        self.name = name # Function name
        self.type = type
        self.scope_level = scope_level
        self.members = {} # Holds data about variables and such

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members[key]

    def get(self, key):
        return self.members.get(key)


class ARType(Enum):
    GLOBAL = 0
    FUNCTION = 1
    IfBlock = 2


"""
AR Types: <- str
 - global
 - function
 - ifblock
"""

################################
# INTERPRETER
################################


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = None
    
    def interpret(self):
        try:
            self.visit(self.tree)
            return 'success'
        except Exception as exc:
            raise exc

    def visit_Block(self, node):
        if self.call_stack is None: # Create a global scope
            self.call_stack = CallStack()
            ar = ActivationRecord(
                name='global',
                type=ARType.GLOBAL,
                scope_level=1,
            )
            self.call_stack.push(ar)

        for child in node.children:
            self.visit(child)

        curr_ar = self.call_stack.peek()
        if curr_ar.name == 'global':
            self.call_stack.pop()

    def visit_BinOp(self, node):
        if isinstance(type(self.visit(node.left)), bool) or isinstance(type(self.visit(node.right)), bool):
            raise Exception("Error: Can not run {} operation on types {} {}".format(
                 node.op.value, node.left.value, node.right.value
            ))
        if node.op.value == '+':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.value == '-':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.value == '/':
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.value == '*':
            return self.visit(node.left) * self.visit(node.right)
    
    def visit_FuncDecl(self, node):
        pass 

    def visit_FuncCall(self, node):
        func_name = node.func_name
        func_symbol = node.func_symbol

        ar = ActivationRecord(
            name=func_name,
            type=ARType.FUNCTION,
            scope_level=func_symbol.scope_level + 1
        )

        formal_params = func_symbol.formal_params
        actual_params = node.params

        for f_param_symbol, a_param_node in zip(formal_params, actual_params):
            ar.members[f_param_symbol.name] = self.visit(a_param_node)

        self.call_stack.push(ar)

        # Visit function block
        self.visit(func_symbol.block)

        # check if function should return anything
        ar = self.call_stack.peek()
        returns = ar['return']
        if returns is not None and len(returns) == 1:
            returns = returns[0]
        

        self.call_stack.pop()
        return returns

        
    def visit_Returns(self, node):
        ar = self.call_stack.peek()

        if ar.type == ARType.GLOBAL:
            raise Exception(
                'Error: Invalid syntax'
            )

        returns = []
        for item in node.returns:
            value = self.visit(item)
            returns.append(value)

        ar.members['return'] = returns


    def visit_Assign(self, node):
        var_name = node.name.value
        var_value = self.visit(node.value)
        ar = self.call_stack.peek() # Save in ar at the top of the stack
        ar.members[var_name] = var_value

    def visit_IfStatement(self, node): # Will not have separate AR
        if self.visit(node.value): # Check if block should run
            self.visit(node.block)
        else:
            if node.elseblock is not None:
                self.visit(node.elseblock)
        
    def visit_Var(self, node):
        var_name = node.value
        ar = self.call_stack.peek()
        var_value = ar.get(var_name)
        return var_value

    def visit_Comparison(self, node):
        op = node.op.value
        left = self.visit(node.left)
        right = self.visit(node.right)

        if op == '<':
            return self.visit(node.left) < self.visit(node.right)
        if op == '<=':
            return self.visit(node.left) <= self.visit(node.right)
        if op == '>=':
            return self.visit(node.left) >= self.visit(node.right)
        if op == '>':
            return self.visit(node.left) > self.visit(node.right)
        if op == '==':
            return self.visit(node.left) == self.visit(node.right)

    def visit_Print(self, node):
        i = 0
        print_str = ''
        while i <= len(node.args) - 1:
            current_arg = self.visit(node.args[i])
            if type(current_arg).__name__ == 'list':
                for item in current_arg:
                    print_str += str(item)
            
            else:
                print_str += str(current_arg)

            i += 1

        print(print_str)

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_Empty(self, node):
        # Do nothing on empty statement
        pass










