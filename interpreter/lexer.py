#######################################
#######################################
# LEXER
#######################################
#######################################

# Define the symbols and built in names

symbols = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    'EOF': 'EOF',
    '=': 'EQUAL',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    ';': 'SCOLON',
    '>': 'GRTHAN',
    '<': 'LSTHAN',
    ':': 'COLON',
    # Double equal is used for comparison
    # Single equal is used for assignment
    '==': 'ISEQUAL',
    '>=': 'GRTHEQ',
    '<=': 'SMTHEQ'
}

# Other token types
other_types = {
    'name': 'NAME',
    # Represents a bool value not 
    # a type declaration of boolean
    'bool': 'BOOL',
    'id': 'ID',
    'type_decl': 'TYPE_DECL'
}

# Special reserved words
reserved_names = {
    'print': 'PRINT',
    'else': 'ELSE',
    'if': 'IF',
    'str': 'TYPE',
    'int': 'TYPE',
    'bool': 'TYPE',
    'float': 'TYPE',
    'True': 'BOOL',
    'False': 'BOOL',
    'function': 'FUNCDECL',
    'return': 'RETURN'
}


class Token(object):
    def __init__(self, token_type, value):
        self.value = value
        self.type = token_type

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


# Lexer reads the text file and generates a stream 
# of tokens as they follow one another that we can than 
# feed to the parser
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('SyntaxError: Invalid syntax')

    def advance(self):
        if self.pos < len(self.text) - 1:
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.pos += 1
            self.current_char = None

    # Allows us to look one char ahead
    def peek(self):
        if self.pos < len(self.text) - 1:
            new_pos = self.pos + 1
            next_char = self.text[new_pos]
            return next_char
        return None

    def skip_whitespace(self):
        # Skips all the whitespaces
        while True:
            self.advance()
            if self.current_char is None:
                break
            if not self.current_char.isspace():
                break

    # Returns tokens one by one
    def get_next_token(self):
        print('char: ', self.current_char)
        # Check for end of file
        if self.pos > len(self.text) - 1:
            return Token('EOF', None)

        # Skip whitespaces
        if self.current_char.isspace():
            self.skip_whitespace()

            # Check for EOF otherwise there is an error if you leave 
            # empty lines at the end of the file
            if self.current_char == None and self.pos > len(self.text) - 1:
                return Token('EOF', None)

        # First check for symbols
        symbol = symbols.get(self.current_char)
        if symbol is not None:
            char = self.current_char

            # Check for comparisons
            if char == '=':
                next_char = self.peek()
                if next_char == '=':
                    for _ in range(2):
                        self.advance()
                    return Token('ISEQUAL', '==')
            
            if char == '>':
                next_char = self.peek()
                if next_char == '=':
                    for _ in range(2):
                        self.advance()
                    return Token('GRTHEQ', '>=')

            
            if char == '<':
                next_char = self.peek()
                if next_char == '=':
                    for _ in range(2):
                        self.advance()
                    return Token('SMTHEQ', '<=')

            self.advance()
            return Token(symbol, char)

        # Check for integers
        if self.current_char.isdigit():
            print('jakob1')
            token = self.integer()
            print(token)
            return token

        # Check for names -> including built-in names
        if self.current_char.isalpha():
            token = self.name()
            return token

        # Check for strings
        # Strings can be defined by '' or ""
        if self.current_char == '"' or self.current_char == "'":
            token = self.string()
            return token

        return self.error()

    def integer(self):
        is_float = False
        int_string = self.current_char
        self.advance()

        if self.current_char is not None:
            while True:
                char = self.current_char
                if not char.isdigit() and not char == '.':
                    break
                int_string += char
                if char == '.': # Check for float
                    is_float = True 
                self.advance()

                # Handle EOF
                if self.current_char is None:
                    break
        
        if is_float:               
            int_value = float(int_string)
            return Token('FLOAT', int_value)
        else:
            int_value = int(int_string)
            return Token('INTEGER', int_value)

    def name(self):
        name = self.current_char
        self.advance()

        if self.current_char is not None:
            while True:
                char = self.current_char
                if char != '_' and not char.isalpha():
                    break
                name += char
                self.advance()

                # Handle EOF
                if self.current_char is None:
                    break

        # Check for builtin names
        if reserved_names.get(name) is not None:
            # Check for booleans
            if name == 'True':
                value = True
            elif name == 'False':
                value = False
            else:
                value = name
            return Token(reserved_names[name], value)

        return Token('NAME', name)

    def string(self):
        opening_tag = self.current_char
        self.advance()
        string = ''

        while True:
            char = self.current_char
            if char == opening_tag:
                break
            string += char
            self.advance()

        # Advance for the closing tag
        self.advance()
        return Token('STRING', string)
