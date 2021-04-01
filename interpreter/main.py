from lexer import Lexer

def main():
    text = 'print("Hello World", 4);'
    lexer_check = Lexer(text)
    while True:
        token = lexer_check.get_next_token()
        print(token)
        if token.type == 'EOF':
            break  


if __name__ == "__main__":
    main()