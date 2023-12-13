MAX_PALABRA = 50
MAX_PALABRAS = 10000
RESERVADAS = 11
OPRELACIONAL = 3
OPARITMETICO = 4
HEXADECIMAL = 16
ALFABETO = 52

compila = 1
iterador = 0
finRep = 0
siNo = 0
finSi = 0
finProg = 0

palabraReservada = ["PROGRAMA", "FINPROG", "SI", "ENTONCES", "SINO", "FINSI", "REPITE", "VECES", "FINREP", "IMPRIME", "LEE"]
hexadecimal = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
operadorRelacional = ["<", ">", "=="]
operadorAritmetico = ["+", "-", "/", "*"]
asignacion = ["="]
literalTexto = ["literalTexto"]
literalNumerica = ["literalNumerica"]
identificador = ["identificador"]
operadorAri = ["operadorAritmetico"]
operadorRel = ["operadorRelacional"]
token = ["" for _ in range(MAX_PALABRA)]
tokens = [["" for _ in range(MAX_PALABRA)] for _ in range(MAX_PALABRAS)]
indice = 0
analisisLexico = 1
aux = 0


def error():
    print("*El programa está escrito incorrectamente.*")


def Prog():
    global iterador, compila
    if tokens[iterador][0] == "PROGRAMA" and iterador + 1 < len(tokens) and tokens[iterador + 1][0] == identificador[0]:
        iterador += 2
        Sents()
    if iterador < len(tokens) and tokens[iterador][0] == "FINPROG":
        compila = 0


def Sents():
    Sent()
    if tokens[iterador] != "FINPROG" and tokens[iterador] != "SINO" and tokens[iterador] != "FINSI" and tokens[iterador] != "FINREP":
        Sents()


# ...

def Sent():
    global iterador, compila
    if tokens[iterador][0] == identificador[0] and tokens[iterador + 1][0] == asignacion[0] and (
            tokens[iterador + 2][0] == identificador[0] or tokens[iterador + 2][0] == literalNumerica[0]) and tokens[
        iterador + 3][0] == operadorAri[0] and (
            tokens[iterador + 4][0] == identificador[0] or tokens[iterador + 4][0] == literalNumerica[0]):
        for _ in range(5):
            iterador += 1
    elif tokens[iterador][0] == identificador[0] and tokens[iterador + 1][0] == asignacion[0] and (
            tokens[iterador + 2][0] == identificador[0] or tokens[iterador + 2][0] == literalNumerica[0]):
        for _ in range(3):
            iterador += 1
    elif tokens[iterador][0] == "SI" and tokens[iterador + 1][0] == identificador[0] and tokens[iterador + 2][0] == operadorRel[0] and (
            tokens[iterador + 3][0] == identificador[0] or tokens[iterador + 3][0] == literalNumerica[0]) and tokens[
        iterador + 4][0] == "ENTONCES":
        for _ in range(5):
            iterador += 1
        Sents()
        if tokens[iterador][0] == "SINO":
            iterador += 1
            Sents()
            if tokens[iterador][0] == "FINSI":
                iterador += 1
            else:
                compila = 0
        elif tokens[iterador][0] == "FINSI":
            iterador += 1
        else:
            compila = 0
    elif tokens[iterador][0] == "REPITE" and (
            tokens[iterador + 1][0] == identificador[0] or tokens[iterador + 1][0] == literalNumerica[0]) and tokens[
        iterador + 2][0] == "VECES":
        for _ in range(3):
            iterador += 1
        Sents()
        if tokens[iterador][0] == "FINREP":
            iterador += 1
        else:
            compila = 0
            iterador += 1
    elif tokens[iterador][0] == "IMPRIME" and (
            tokens[iterador + 1][0] == identificador[0] or tokens[iterador + 1][0] == literalNumerica[0]):
        iterador += 2
    elif tokens[iterador][0] == "IMPRIME" and tokens[iterador + 1][0] == literalTexto[0]:
        iterador += 2
    elif tokens[iterador][0] == "LEE" and tokens[iterador + 1][0] == identificador[0]:
        iterador += 2
    else:
        compila = 0
        iterador += 1


# Código principal
# Lectura del archivo programa.mio
nombreArchivo = "programa.mio"
try:
    with open(nombreArchivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            # Ignorar líneas que empiecen con "#"
            if linea[0] == '#':
                continue
            # Crear arreglo con cada palabra
            tokens[indice] = linea.split()
            indice += 1
except FileNotFoundError:
    print(f"No se pudo abrir el archivo {nombreArchivo}. Verifica la ruta y el nombre del archivo.")
    exit()
except UnicodeDecodeError as e:
    print(f"Error al decodificar el archivo: {e}")
    exit()
 

# Definir tipo de palabra o cadena y hacer análisis léxico
for x in range(indice):
    tipoDef = 0
    esNumero = 1
    if tokens[aux][0] == '"':
        finTexto = 1
        tokens[x] = literalTexto
        if len(tokens[aux]) == 1:
            aux += 1
            indice -= 1
        while finTexto:
            if tokens[aux][-1] == '"':
                finTexto = 0
            else:
                aux += 1
                indice -= 1
    else:
        for y in range(RESERVADAS):
            if tokens[aux][0] == palabraReservada[y][0] and tokens[aux] == palabraReservada[y]:
                tokens[x] = palabraReservada[y]
                tipoDef = 1
        if not tipoDef:
            for y in range(OPRELACIONAL):
                if tokens[aux][0] == operadorRelacional[y][0] and tokens[aux] == operadorRelacional[y]:
                    tokens[x] = operadorRel
                    tipoDef = 1
        if not tipoDef:
            for y in range(OPARITMETICO):
                if tokens[aux][0] == operadorAritmetico[y][0] and tokens[aux] == operadorAritmetico[y]:
                    tokens[x] = operadorAri
                    tipoDef = 1
        if not tipoDef and tokens[aux][0] == asignacion[0] and tokens[aux] == asignacion:
            tokens[x] = asignacion
            tipoDef = 1
        if not tipoDef and tokens[aux][0] == '0' and tokens[aux][1] == 'x' and len(tokens[aux]) > 2:
            num = ''.join(tokens[aux][2:])
            if all(c in hexadecimal for c in num):
                tokens[x] = literalNumerica
                tipoDef = 1

        if not tipoDef and tokens[aux][0].isalpha() and len(tokens[aux]) < 17:
            tokens[x] = identificador
            tipoDef = 1
        if not tipoDef:
            analisisLexico = 0
    aux += 1


# Análisis Sintáctico
if analisisLexico:
    Prog()
else:
    compila = 0

if not compila:
    error()
else:
    print("El programa está escrito correctamente.")