#Lexer..........................................
# Lista de Tokens
tokens = ('IDENTIFICADOR','NUMERO','SUMA','RESTA','MULTIPLICACION','DIVISION',
          'ASIGNACION','MENOR','MENORQUE','MAYOR','MAYORQUE',
          'PARENTESIS_IZQ','PARENTESIS_DER','COMA','PUNTO_Y_COMA','PUNTO',
          'LLAVE_IZQ','LLAVE_DER' 
)

# Palabras Reservadas #
reservadas = (
    'SI',
    'SINO',
    'MIENTRAS',
    'DO',
    'ENTERO',
    'PARA',
    'IN'
)

tokens = tokens+reservadas

# Expresiones Regulares para tokens Simples

t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_ASIGNACION = r':='
t_MENOR = r'<'
t_MENORQUE = r'<='
t_MAYOR = r'>'
t_MAYORQUE = r'>='
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_COMA = r','
t_PUNTO_Y_COMA = r';'
t_PUNTO = r'\.'
t_LLAVE_IZQ = r'\['
t_LLAVE_DER = r'\]'

def t_SI(t):
    r'if'
    return t
# Expresion Regular para Cualquier cantidad de letras de variable
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    return t

# para que acepte comentarios
def t_COMMENT(t):
    r'\#.*'
    pass

# Expresion regular para cualquier cantidad de numeros enteros
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newLine(t):
    # Define Saltos de Lineas
    r'\n+'
    t.lexer.lineno += len(t.value)

# Cadena de caracteres a ignorar (espacios, tabulaciones y saltos de linea)
t_ignore = ' \t'


def t_error(t):
    # Manejo de errores, si un caracter de entrada no coincide con los tokens
    # este metodo indica cual es ese caracter
    global respuesta_Parser
    resultado = "Caracter Invalido '%s'" % t.value[0]
    respuesta_Parser.append(resultado)
    t.lexer.skip(1)

# Instanciamos el Analizador Lexico.
import ply.lex as lex
lexer = lex.lex()



# Reglas del Parser.
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('right', 'UMINUS'),
)

# Diccionario de Nombres
nombres = {}

respuesta_Parser = []

def p_declaracion_asignacion(p):
    "declaracion : IDENTIFICADOR ASIGNACION expresion"
    nombres[p[1]] = p[3]


def p_declaracion_expresion(p):
    "declaracion : expresion"
    global respuesta_Parser
    respuesta_Parser.append(p[1])

def p_expresion_uminus(p):
    "expresion : '-' expresion %prec UMINUS"
    p[0] = -p[2]

def p_expresion_grupo(p):
    "expresion : PARENTESIS_IZQ expresion PARENTESIS_DER"
    p[0] = p[2]

def p_prueba(p):
    '''
    expresion : expresion RESTA expresion
              | expresion SUMA expresion
              | expresion MAYOR expresion
              | expresion MENOR expresion
              | expresion MENORQUE expresion
              | expresion MAYORQUE expresion
              | expresion MULTIPLICACION expresion
              | expresion DIVISION expresion
              | expresion IN expresion
    '''
    pass

def p_condi_ciclos(p):
    '''
    declaracion  : SI expresion  LLAVE_IZQ  LLAVE_DER
                | SI expresion  LLAVE_IZQ declaracion LLAVE_DER
                | SI expresion  LLAVE_IZQ expresion LLAVE_DER
                | SINO expresion  LLAVE_IZQ  LLAVE_DER
                | SINO expresion  LLAVE_IZQ declaracion LLAVE_DER
                | SINO expresion  LLAVE_IZQ expresion LLAVE_DER
                | MIENTRAS expresion  LLAVE_IZQ  LLAVE_DER
                | MIENTRAS expresion  LLAVE_IZQ declaracion LLAVE_DER
                | MIENTRAS expresion  LLAVE_IZQ expresion LLAVE_DER
                | PARA expresion  LLAVE_IZQ  LLAVE_DER
                | PARA expresion  LLAVE_IZQ declaracion LLAVE_DER
                | PARA expresion  LLAVE_IZQ expresion LLAVE_DER
                | DO expresion  LLAVE_IZQ  LLAVE_DER
                | DO expresion  LLAVE_IZQ declaracion LLAVE_DER
                | DO expresion  LLAVE_IZQ expresion LLAVE_DER
                | SI expresion  LLAVE_IZQ declaracion expresion LLAVE_DER
                | SI expresion  LLAVE_IZQ expresion declaracion LLAVE_DER
                | SINO expresion  LLAVE_IZQ declaracion expresion LLAVE_DER
                | SINO expresion  LLAVE_IZQ expresion declaracion LLAVE_DER
                | MIENTRAS expresion  LLAVE_IZQ declaracion expresion LLAVE_DER
                | MIENTRAS expresion  LLAVE_IZQ expresion declaracion LLAVE_DER
                | PARA expresion  LLAVE_IZQ declaracion expresion LLAVE_DER
                | PARA expresion  LLAVE_IZQ declaracion declaracion LLAVE_DER
                | PARA expresion  LLAVE_IZQ expresion declaracion LLAVE_DER
                | DO expresion  LLAVE_IZQ declaracion expresion LLAVE_DER
                | DO expresion  LLAVE_IZQ expresion declaracion LLAVE_DER
                
                
    '''
    global respuesta_Parser
    respuesta_Parser.append('Correcto')


def p_expresion_numero(p):
    "expresion : NUMERO"
    p[0] = p[1]

def p_expresion_nombre(p):
    "expresion : IDENTIFICADOR"
    global respuesta_Parser
    try:
        p[0] = nombres[p[1]]
    except LookupError:
        resultado = "Nombre no Definido '%s'" % p[1]
        respuesta_Parser.append(resultado)
        p[0] = 0

def p_error(p):
    global respuesta_Parser
    if p:
        resultado = "Error de Sintaxis en '%s'" % p.value
        respuesta_Parser.append(resultado)
    else:
        resultado = "Error de Sintaxis en EOF"
        respuesta_Parser.append(resultado)

import ply.yacc as yacc
parser = yacc.yacc()
