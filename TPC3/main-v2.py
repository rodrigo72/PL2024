import ply.lex as lex
import sys

tokens = (
    'ON',
    'OFF',
    'EQUALS',
    'NUMBER',
    'OTHER'
)

states = (
    ('on', 'exclusive'),
    ('off', 'exclusive')
)

count = 0

t_ignore = ' \t\n'
t_on_off_ignore = ' \t\n'    
    

def t_on_off_ON(t):
    r'(?i)on'
    t.lexer.begin('on')
    return t
    

def t_on_off_OFF(t):
    r'(?i)off'
    t.lexer.begin('off')
    return t
    

def t_on_off_EQUALS(t):
    r'\='
    print(count)
    return t
    

def t_on_NUMBER(t):
    r'\d+'
    global count
    count += int(t.value)
    return t


def t_off_NUMBER(t):
    r'\d+'
    return t


def t_on_off_OTHER(t):
    r'((?!(?:\d|on|off|=)).)+'  # or just r'.'
    return t


def t_OTHER(t):
    r'.'
    return t


def t_ANY_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)


def main():
    lexer = lex.lex();
    lexer.begin('on')
    
    data = sys.stdin.read()
    lexer.input(data)
    for tok in lexer:
        print(tok)


if __name__ == '__main__':
    main()
