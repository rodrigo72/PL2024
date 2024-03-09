import sys
import ply.lex as lex

# documentation: http://www.dabeaz.com/ply/ply.html#ply_nn6
reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'and': 'AND',
    'or': 'OR',
}

# order matters
tokens = [
    'NUMBER',
    'MATH_OPERATOR',
    'FIELD',
    'FIELD_NAME',
    'TABLE',
    'TABLE_NAME',
    'SKIP',
    'LPAREN',
    'RPAREN',
    'DELIMITER',
    'FINAL_DELIMITER',
 ] + list(reserved.values())


# uppercase in the function name matters
def t_NUMBER(t):
    r"""([\+\-]?\d+(?:\.\d+)?)"""
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


def t_MATH_OPERATOR(t):
    r""">=|<=|\+|-|\*|>|<|="""
    return t


def keyword_type(t):
    match t.type:
        case "SELECT":
            t.lexer.prev_val = "FIELD_NAME"
        case "FROM":
            t.lexer.prev_val = "TABLE_NAME"
        case "WHERE":
            t.lexer.prev_val = "FIELD_NAME"
        case _:
            print("Error")
    return t


def t_FIELD(t):
    r"""\w+"""
    t.type = reserved.get(t.value.lower(), t.lexer.prev_val)
    if t.type != t.lexer.prev_val:
        t = keyword_type(t)
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DELIMITER = r","
t_FINAL_DELIMITER = r";"
t_SKIP = r"\s"


def t_error(t):
    sys.stderr.write(f"Error: Unexpected character {t.value[0]}\n")
    t.lexer.skip(1)


def main():
    _lexer = lex.lex()
    _lexer.prev_val = ""

    for line in sys.stdin:
        _lexer.input(line)
        for token in _lexer:
            if not token:
                break
            print(token)


if __name__ == "__main__":
    main()
