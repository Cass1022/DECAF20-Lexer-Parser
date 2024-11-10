import ply.lex as lex
import sys


tokens = [
    'AND',  # &&
    'ASSIGN',  # =
    'BOOLTYPE',  # bool
    'BREAK',  # break
    'CHARCONSTANT',  # char_lit (see section on Character literals)
    'COMMA',  # ,
    'COMMENT',  # comment
    'CONTINUE',  # continue
    'DIV',  # /
    'DOT',  # .
    'ELSE',  # else
    'EQ',  # ==
    'EXTERN',  # extern
    'FALSE',  # false
    'FOR',  # for
    'FUNC',  # func
    'GEQ',  # >=
    'GT',  # >
    'ID',  # identifier (see section on Identifiers)
    'IF',  # if
    'INTCONSTANT',  # int_lit (see section on Integer literals)
    'INTTYPE',  # int
    'LCB',  # {
    'LEFTSHIFT',  # <<
    'LEQ',  # <=
    'LPAREN',  # (
    'LSB',  # [
    'LT',  # <
    'MINUS',  # -
    'MOD',  # %
    'MULT',  # *
    'NEQ',  # !=
    'NOT',  # !
    'NULL',  # null
    'OR',  # ||
    'PACKAGE',  # package
    'PLUS',  # +
    'RCB',  # }
    'RETURN',  # return
    'RIGHTSHIFT',  # >>
    'RPAREN',  # )
    'RSB',  # ]
    'SEMICOLON',  # ;
    'STRINGCONSTANT',  # string_lit (see section on String literals)
    'STRINGTYPE',  # string
    'TRUE',  # true
    'VAR',  # var
    'VOID',  # void
    'WHILE',  # while
    'WHITESPACE',  # whitespace (see section on Whitespace)
]

# Reserved statements to reduce number of regular expressions
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'func': 'FUNC',
    'null': 'NULL',
    'package': 'PACKAGE',
    'return': 'RETURN',
    'extern': 'EXTERN',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'var': 'VAR',
    'void': 'VOID',
    'whitespace': 'WHITESPACE',
}

# Token methods for matching during analysis

def t_STRINGCONSTANT(t):
    r'"(\\.|[^"\\])*"'
    t.value = str(t.value)
    return t


def t_AND(t):
    r'&&'
    t.value = '&&'
    return t


def t_CHARCONSTANT(t):
    r"'(\\.|[^\\'])\'"
    t.value = str(t.value)
    return t


def t_BOOLTYPE(t):
    r'bool'
    t.value = 'bool'
    return t


def t_COMMA(t):
    r','
    t.value = ','
    return t


def t_COMMENT(t):
    r'\/\/[^\n]*'
    pass


def t_DIV(t):
    r'/'
    t.value = '/'
    return t


def t_DOT(t):
    r'\.'
    t.value = '.'
    return t


def t_EQ(t):
    r'=='
    t.value = '=='
    return t


def t_GEQ(t):
    r'>='
    t.value = '>='
    return t



def t_ASSIGN(t):
    r'='
    t.value = '='
    return t


def t_RIGHTSHIFT(t):
    r'>>'
    t.value = '>>'
    return t


def t_GT(t):
    r'>'
    t.value = '>'
    return t


def t_INTCONSTANT(t):
    r'0[xX][0-9a-fA-F]+|(\d+([uU]|[lL]|[uU][lL]|[lL][uU])?)'
    t.value = str(t.value)
    return t


def t_INTTYPE(t):
    r'int'
    t.value = 'int'
    return t


def t_STRINGTYPE(t):
    r'string'
    t.value = 'string'
    return t


def t_LCB(t):
    r'{'
    t.value = '{'
    return t


def t_LEFTSHIFT(t):
    r'<<'
    t.value = '<<'
    return t


def t_LEQ(t):
    '<='
    t.value = '<='
    return t


def t_LPAREN(t):
    r'\('
    t.value = '('
    return t


def t_LSB(t):
    r'\['
    t.value = '['
    return t


def t_LT(t):
    r'<'
    t.value = '<'
    return t


def t_MINUS(t):
    r'-'
    t.value = '-'
    return t


def t_MOD(t):
    r'%'
    t.value = '%'
    return t


def t_MULT(t):
    r'\*'
    t.value = '*'
    return t


def t_NEQ(t):
    r'!='
    t.value = '!='
    return t


def t_NOT(t):
    r'!'
    t.value = '!'
    return t


def t_OR(t):
    r'\|\|'
    t.value = '||'
    return t


def t_PLUS(t):
    r'\+'
    t.value = '+'
    return t


def t_RCB(t):
    r'}'
    t.value = '}'
    return t


def t_RPAREN(t):
    r'\)'
    t.value = ')'
    return t


def t_RSB(t):
    r'\]'
    t.value = ']'
    return t


def t_SEMICOLON(t):
    r';'
    t.value = ';'
    return t


def t_WHITESPACE(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Error statement if illegal characters occur

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at index {t.lexpos}")
    t.lexer.skip(1)

# Builds the lexer
lexer = lex.lex()

# Keeps track of which line the token is on
def find_row(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr

# Output
def print_tokens(lexer, input_data):
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Keeps tack of column space taken up by tokens
        start_column = find_row(input_data, tok)
        end_column = start_column + len(tok.value) - 1

        print(f"Line {tok.lineno} | Columns {start_column}-{end_column} is {tok.type} ({tok.value})")


def main(example):
    with open(example, 'r') as file:
        data = file.read()
        print("------------------" + str(file.name) + "---------------------")
        lexer.input(data)
        print_tokens(lexer, data)


if __name__ == '__main__':
    # example = sys.argv[1]
    example = 'test.decaf'
    main(example)
