from rply import LexerGenerator

TOKENS = ['START', 'DONE', 'NEXT', 'LPAREN', 'RPAREN', 'LBRACE',
          'RBRACE', 'LBRACKET', 'RBRACKET', 'COLON', 'SEMI',
          'LEFT_ARROW', 'EQUAL', 'COMMA', 'ADD', 'SUB', 'MOD',
          'NOT_EQ', 'NUMBER', 'ID' ]

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('START', r'start')
        self.lexer.add('DONE', r'done')
        self.lexer.add('NEXT', r'next')

        # Parenthesis, assorted
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')

        self.lexer.add('LBRACE', r'\{')
        self.lexer.add('RBRACE', r'\}')

        self.lexer.add('LBRACKET', r'\[')
        self.lexer.add('RBRACKET', r'\]')

        # Delimiters
        self.lexer.add('COLON', r'\:')
        self.lexer.add('SEMI', r'\;')
        self.lexer.add('LEFT_ARROW', r'<=')
        self.lexer.add('EQUAL', r'=')
        self.lexer.add('COMMA', r',')

        # Operators
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MOD', r'mod')
        self.lexer.add('NOT_EQ', r'\!\=')

        # Number
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('ID', r'[\w|_]+')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
