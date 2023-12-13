import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser
from nltk.tokenize import word_tokenize

#definir la grámatica del lenguaje "mio"

grammar = CFG.fromstring("""
   PROG -> "PROGRAMA" ID SENTS "FINPROG"
   SENTS -> SENT SENTS | SENT
   SENT -> ASSIGN | CONDITIONAL | LOOP | PRINT | READ | COMMENT
   ASSIGN -> ID "=" ELEM
   CONDITIONAL -> "SI" COMPARA "ENTONCES" SENTS "SINO" SENTS "FINSI" | "SI" COMPARA "ENTONCES" SENTS "FINSI"
   LOOP -> "REPITE" ELEM "VECES" SENTS "FINREP"
   PRINT -> "IMPRIME" ELEM | "IMPRIME" TXT
   READ -> "LEE" ID
   COMMENT -> "#" TXT
   ELEM -> ID | VAL | TXT
   COMPARA -> ID OP_REL ELEM
   OP_REL -> ">" | "<" | "=="
   ID -> '[a-zA-Z][a-zA-Z0-9_.]*' | "[a-zA-Z][a-zA-Z0-9_.]*"
   VAL -> '0[xX][0-9a-fA-F]+' | '[0-9]+'
   TXT -> '\"[^\"]*\"'
""")

# Crear un analizador sintáctico

parser = RecursiveDescentParser(grammar)

def sintactico(file_path):

    # Leer el archivo
    with open(file_path, 'r') as file:
        programa = file.read()

    #tokens = word_tokenize(programa)
    #print("Tokens:", tokens)  # Imprime los tokens para ayudar a depurar
    #parser = EarleyChartParser(grammar)


    try:
        for tree in parser.parse(word_tokenize(programa)):
            print("El programa está escrito correctamente.")
            print(tree)
            return True
        
    except ValueError as e:
        print(f"Error de sintaxis: {e}")


sintactico("programa.mio")