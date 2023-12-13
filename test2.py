import nltk
import re
from nltk import CFG
from nltk.parse import EarleyChartParser
from nltk.tokenize import word_tokenize

# Definición de las palabras reservadas, operadores y otros elementos del lenguaje MIO
reserved_words = ['PROGRAMA', 'FINPROG', 'SI', 'ENTONCES', 'SINO', 'FINSI', 'REPITE', 'VECES', 'FINREP', 'IMPRIME', 'LEE']
relational_operators = ['>', '<', '==', '=']
arithmetic_operators = ['+', '-', '*', '/']

# Definición de los tokens
def define_tokens(program):
    tokens = []
    lines = program.split('\n')
    for line in lines:
        if line.startswith('#'):
            tokens.append(('comentario', line[1:]))
        else:
            words = line.split(' ')
            for word in words:
                if word in reserved_words:
                    tokens.append(('reserved_word', word))
                elif word in relational_operators:
                    tokens.append(('op_rel', word))
                elif word in arithmetic_operators:
                    tokens.append(('op_ar', word))
                elif re.match(r'^0x[0-9A-F]+$', word):
                    tokens.append(('val', word))
                elif re.match(r'^".*"$', word):
                    tokens.append(('txt', word))
                elif re.match(r'^[a-zA-Z][a-zA-Z0-9]{0,15}$', word):
                    tokens.append(('id', word))
    return tokens

# Definición de la gramática del lenguaje MIO
grammar = nltk.CFG.fromstring("""
    PROG -> 'PROGRAMA' 'id' SENTS 'FINPROG'
    SENTS -> SENT SENTS | SENT
    SENT -> 'id' '=' ELEM 'op_ar' ELEM | 'id' '=' ELEM | 'SI' COMPARA 'ENTONCES' SENTS 'SINO' SENTS 'FINSI' | 'SI' COMPARA 'ENTONCES' SENTS 'FINSI' | 'REPITE' ELEM 'VECES' SENTS 'FINREP' | 'IMPRIME' ELEM | 'IMPRIME' 'txt' | 'LEE' 'id' | '#' 'comentario'
    ELEM -> 'id' | 'val'
    COMPARA -> 'id' 'op_rel' ELEM
""")

def sintactico(file_name):
    # Leer el archivo del programa MIO
    with open(file_name, 'r') as file:
        program = file.read()

    # Definir los tokens
    tokens = define_tokens(program)

    # Crear un analizador sintáctico con la gramática del lenguaje MIO
    parser = nltk.ChartParser(grammar)

    # Analizar el programa
    
    try:
        for tree in parser.parse(tokens):
            print("El programa está escrito correctamente.")
            print(tree)
            return True
        
    except ValueError as e:
        print(f"Error de sintaxis: {e}")    

sintactico("programa.mio")
