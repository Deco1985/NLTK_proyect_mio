# Importar la librería NLTK
import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser
nltk.download('punkt')
import re



#En esta celda se verifican los identificadores de cadena

# Identificadores
identificador = r'[a-zA-Z][a-zA-Z0-9]{0,15}'

# Literales de texto
literal_texto = r'\".*\"'

# Literales numéricas
literal_numerica = r'0x[0-9A-Fa-f]+'

# Función para verificar si una cadena es un identificador
def es_identificador(cadena):
    return re.fullmatch(identificador, cadena) is not None

# Función para verificar si una cadena es un literal de texto
def es_literal_texto(cadena):
    return re.fullmatch(literal_texto, cadena) is not None

# Función para verificar si una cadena es un literal numérico
def es_literal_numerica(cadena):
    return re.fullmatch(literal_numerica, cadena) is not None

# Prueba las funciones
print(es_identificador('DiaDeLaSemana1'))  # Debería imprimir True
print(es_literal_texto('"caracteres alf4num3ric05"'))  # Debería imprimir True
print(es_literal_numerica('0x1F'))  # Debería imprimir True



# Definir los tokens
tokens = {
    "reserved_words": ["PROGRAMA", "FINPROG", "SI", "ENTONCES", "SINO", "FINSI", "REPITE", "VECES", "FINREP", "IMPRIME", "LEE"],
    "op_rel": [">", "<", "==", "="],
    "op_ar": ["+", "-", "*", "/"],
    "comment": "#",
    "id": es_identificador,  # Agregar la función de verificación de identificadores
    "txt": es_literal_texto,  # Agregar la función de verificación de literales de texto
    "val": es_literal_numerica  # Agregar la función de verificación de literales numéricos
}



# Definir la gramática
grammar = CFG.fromstring("""
    PROG -> 'PROGRAMA' 'id' SENTS 'FINPROG'
    SENTS -> SENT SENTS | SENT
    SENT -> 'id' '=' ELEM 'op_ar' ELEM | 'id' '=' ELEM | 'SI' COMPARA 'ENTONCES' SENTS 'SINO' SENTS 'FINSI' | 'SI' COMPARA 'ENTONCES' SENTS 'FINSI' | 'REPITE' ELEM 'VECES' SENTS 'FINREP' | 'IMPRIME' ELEM | 'IMPRIME' 'txt' | 'LEE' 'id' | '#' 'comentario'
    ELEM -> 'id' | 'val'
    COMPARA -> 'id' 'op_rel' ELEM
""")



# Función para tokenizar una cadena de caracteres
def tokenize(string):
    tokenized_string = nltk.word_tokenize(string)
    categorized_tokens = []
    for token in tokenized_string:
        if token in tokens["reserved_words"]:
            categorized_tokens.append(("RESERVED_WORD", token))
        elif token in tokens["op_rel"]:
            categorized_tokens.append(("RELATIONAL_OPERATOR", token))
        elif token in tokens["op_ar"]:
            categorized_tokens.append(("ARITHMETIC_OPERATOR", token))
        elif tokens["id"]:  # Llama a la función con el token como argumento
            categorized_tokens.append(("IDENTIFIER", token))
        elif tokens["txt"]:  # Llama a la función con el token como argumento
            categorized_tokens.append(("TEXT_LITERAL", token))
        elif tokens["val"]:  # Llama a la función con el token como argumento
            categorized_tokens.append(("NUMERIC_LITERAL", token))
        elif token == tokens["comment"]:
            categorized_tokens.append(("COMMENT", token))
        else:
            categorized_tokens.append(("UNKNOWN", token))
    return categorized_tokens

# Prueba la función de tokenización
print(tokenize("VarX = 0x1"))



# Crear un analizador sintáctico
parser = nltk.ChartParser(grammar)

# Función para analizar una cadena de caracteres
def parse(string):

    tokenized_string = tokenize(string)
    try:
        for tree in parser.parse([token for category, token in tokenized_string]):
            print(tree)
        print("La cadena de caracteres pertenece a la gramática.")

    except ValueError as e:
        print("La cadena de caracteres no pertenece a la gramática.")
        print("Error:", str(e))


programa_ejemplo = """
PROGRAMA factorial
VarX = 0x1
VarY = 0x0
LEE Num
REPITE Num VECES
 VarY = VarY + 0x1
 VarX = VarX * VarY
FINREP
IMPRIME “Factorial de ”
IMPRIME Num
IMPRIME “ es “
IMPRIME VarX
FINPROG
"""

# Llama a la función de análisis con programa_ejemplo como argumento
parse(programa_ejemplo)
