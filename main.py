# 3.3 - Tokeniza con Ply
# Tadeo Andrés Willis Lozano
# A00829341

import ply.lex as lex

# Palabras reservadas:
reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'end': 'END',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'do': 'DO',
    'while': 'WHILE',
    'print': 'PRINT',
}

# Lista de tokens:
tokens = [
    'IDENTIFIER', 
    'CONST_INT', 
    'CONST_FLOAT', 
    'CONST_STRING', 
    'COMMENT',
    'OP_EQ', 
    'OP_NEQ', 
    'OP_GE', 
    'OP_LE', 
    'OP_GT', 
    'OP_LT',
    'OP_ASSIGN', 
    'OP_PLUS', 
    'OP_MINUS', 
    'OP_MULT', 
    'OP_DIV',
    'SEMICOL', 
    'COMMA', 
    'COLON', 
    'LPAREN', 
    'RPAREN',
    'LBRACE', 
    'RBRACE', 
    'LBRACKET', 
    'RBRACKET',
] + list(reserved.values())

# Operadores:
t_OP_EQ = r'=='
t_OP_NEQ = r'!='
t_OP_GE = r'>='
t_OP_LE = r'<='
t_OP_GT = r'>'
t_OP_LT = r'<'
t_OP_ASSIGN = r'='
t_OP_PLUS = r'\+'
t_OP_MINUS = r'-'
t_OP_MULT = r'\*'
t_OP_DIV = r'/'

# Puntuacion:
t_SEMICOL = r';'
t_COMMA = r','
t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Ignorar y Espacios y Tabs:
t_ignore = ' \t'

# Tokens como funcion:

# Comentario:
def t_COMMENT(t):
    r'\#.*'
    return t

# String:
def t_CONST_STRING(t):
    r'"[^"\n]*"'
    return t


# Float:
def t_CONST_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    return t

# Int:
def t_CONST_INT(t):
    r'[0-9]+'
    return t


# Identificador: empieza con letra y luego letras, digitos o _.
# Si la palabra esta en reserved se cambia el tipo (ej. while -> WHILE),
# si no, se queda como IDENTIFIER.
def t_IDENTIFIER(t):
    r'[a-zA-Z]\w*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


# Contar lineas:
# PLY no cuenta las lineas solo, aqui se suma 1 por cada salto de linea.
# No tiene return, asi que el salto de linea no se vuelve token.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lista para guardar los errores:
errores = []

# Error:
# Se ejecuta cuando un caracter no coincide con ningun token.
def t_error(t):
    errores.append(f"Error en linea {t.lineno}, posicion {t.lexpos}: simbolo no reconocido '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer:
lexer = lex.lex()

# Lee un archivo, lo tokeniza e imprime los tokens y errores:
def tokenizar_archivo(nombre_archivo):
    # Leer todo el archivo como texto:
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    # Reiniciar el contador de lineas y los errores:
    lexer.lineno = 1
    errores.clear()

    # Darle el texto al lexer:
    lexer.input(codigo)

    # Guardar los tokens en una sola lista:
    lista_tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        lista_tokens.append(tok)

    # imprimir separado por lineas:
    print("==========", nombre_archivo, "==========")
    lineas = codigo.splitlines()
    linea_actual = 0
    for tok in lista_tokens:
        if tok.lineno != linea_actual:
            linea_actual = tok.lineno
            print(f"\nLinea {linea_actual}:    {lineas[linea_actual - 1].strip()}")
        print(f"    {tok.type:<14} value: {tok.value:<12} lexpos: {tok.lexpos}")

    # Imprimir errores al final:
    print("\nErrores:")
    if errores:
        for e in errores:
            print(e)
    else:
        print("Sin errores")
    print()

tokenizar_archivo("prueba.txt")