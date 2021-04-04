import inspect
from interpreter.ast import (
    BinOp,
    Var
)

###############################
# Symbol Tables / Scope Tables
###############################


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
        self.scope_level = 0 


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self): # For nice printing
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class VarSymbol(Symbol):
    def __init__(self, name, type): # type == BuilinTypeSymbol instance
        super(VarSymbol, self).__init__(name, type)

    def __str__(self): # For nice printing
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )

    __repr__ = __str__    


class FunctionSymbol(Symbol):
    def __init__(self, name, block, formal_params=None):
        super(FunctionSymbol, self).__init__(name)
        self.formal_params = formal_params if formal_params is not None else []
        self.block = block
        self.returns = None

    
class SymbolTable(object): # Each scope has a symbol table
    def __init__(self, scope_name, scope_level, parent_scope=None):
        self.symbols = {}
        self.scope_level = scope_level
        self._init_builtins()
        self.scope_name = scope_name
        self.parent_scope = parent_scope

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('int'))
        self.insert(BuiltinTypeSymbol('str'))
        self.insert(BuiltinTypeSymbol('bool'))

    def insert(self, symbol):
        symbol.scope_level = self.scope_level
        self.symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        symbol = self.symbols.get(name)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        # recursively go up the chain and lookup the name
        if self.parent_scope is not None:
            return self.parent_scope.lookup(name)

    def __str__(self):
        symtab_header = 'Symbol table contents'
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__


###############################
# Semantic Analysis 
###############################


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, tree):
        self.current_scope = None
        self.tree = tree

    def analyse(self):
        try:
            self.visit(self.tree)
            return 'success'
        except Exception as exc:
            raise exc
            return 'error'
    
    def type_error(self):
        raise Exception('TypeError: Invalid assignment')
    
    @staticmethod
    def check_for_correct_type(var_type, var_value):
         # Because it is an AST NODE
        try:
            value_type = type(var_value.value).__name__
        except AttributeError:
            value_type = 'int'

        var_type = var_type.value
        print(value_type, ' == ', var_type)
        if value_type == var_type:
            return True
        return False        

    def visit_Block(self, node):
        if self.current_scope is None: # Global scope
            glob_scope = SymbolTable(
                scope_name='global',
                scope_level=1,
                parent_scope=self.current_scope, # None
            )
            self.current_scope = glob_scope

        for child in node.children:
            self.visit(child)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_FuncDecl(self, node):
        func_name = node.func_name.value
        func_symbol = FunctionSymbol(
            name=func_name,
            block=node.block_node
        )
        if node.returns is not None:
            func_symbol.returns = node.returns

        self.current_scope.insert(func_symbol)
        func_scope = SymbolTable(
            scope_name=func_name,
            scope_level=self.current_scope.scope_level + 1,
            parent_scope=self.current_scope,
        )
        self.current_scope = func_scope
        
        # Insert formal_params into function scope
        for param in node.formal_params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.insert(var_symbol)
            func_symbol.formal_params.append(var_symbol)

        self.visit(node.block_node)                                
        self.current_scope = self.current_scope.parent_scope # Leave function scope after visiting

    def visit_FuncCall(self, node):
        # 1. Check if the function was declared
        # 2. Check if the num of giver parameters is what the funciton is expecting
        # 3. Check if they are of the right type
        func_symbol = self.current_scope.lookup(node.func_name) 

        if func_symbol is None:
            raise Exception("Error: Function {} is not declared".format(node.func_name))

        # Save this func symbol to AST to use in the Interpreter
        node.func_symbol = func_symbol
          
        # Check if num of given params matches num of formal (declared) params
        num_of_params = len(node.params) 
        if len(func_symbol.formal_params) != num_of_params: 
            raise Exception("Error: Function {} was expecting {} params but got {}".format(
                node.func_name, len(func_symbol.formal_params), num_of_params
            ))
        
        for actual_param, formal_param in zip(node.params, func_symbol.formal_params):
            if isinstance(actual_param, Var):
                self.visit(actual_param)
                continue
            elif isinstance(actual_param, BinOp) and formal_param.type.name != 'int':
                raise Exception("Error: Type of given arg doesn't match defined arg")
            elif isinstance(actual_param, BinOp) and formal_param.type.name == 'int':
                continue

            elif type(actual_param.value).__name__ != formal_param.type.name: # 'str' or 'bool'...
                print('wrong: ', type(actual_param.value).__name__ , formal_param.type.name)
                raise Exception("Error: Type of given arg doesn't match defined arg")


    def visit_Assign(self, node):
        type_name = node.type.value
        type_symbol = self.current_scope.lookup(type_name)
        var_name = node.name.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, current_scope_only=True): # Check for duplicate symbols
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )   

        if not self.check_for_correct_type(node.type, node.value):
            raise Exception(
                'TypeError: Variable {var} is not of type {type}'.format(var=var_name, type=type_name)      
            )

        self.current_scope.insert(var_symbol)

    
    def visit_Returns(self, node):
        returns = node.returns
        for node in returns:
            self.visit(node)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            ) 
    
    def visit_Print(self, node):
        for arg in node.args:
            self.visit(arg)
 
    def visit_IfStatement(self, node):
        self.visit(node.value)
        self.visit(node.block)
        if node.elseblock:
            self.visit(node.elseblock)

    def visit_Comparison(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Number(self, node):
        value = node.value
        if not isinstance(value, int) and not isinstance(value, float):
            raise Exception("TypeError: '%s' is not a Number" % value)

    def visit_String(self, node):
        value = node.value
        if not isinstance(value, str):
            raise Exception("TypeError: '%s' is not a String" % value)

    def visit_Boolean(self, node):
        value = node.value
        if not isinstance(value, bool):
            raise Exception("TypeError: '%s' is not a Boolean" % value)

    def visit_Empty(self, node):
        # Nothing to do on empty statement
        pass








