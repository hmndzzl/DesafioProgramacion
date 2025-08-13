"""
# MM2015 - Desafío de programación 1: Lógica proposicional
# autor: macastillo

# NOTA:
# Debe utilizar letras minúsculas para los nombres de las variables, por ejemplo, a, b, c.
# Puede utilizar paréntesis para agrupar expresiones, como «a and (b or c)».

# Implemente las cuatro funciones siguientes:
# tabla_verdad, tautologia, equivalentes e inferencia

# Entrega:
# Deberá subir este archivo a la página del curso en Canvas.
"""


######## No modifique el siguiente bloque de código ########
# ********************** COMIENZO *******************************

from functools import partial
import re


class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

@Infix
def implies(p, q) :
    return not p or q

@Infix
def iff(p, q) :
    return (p |implies| q) and (q |implies| p)

# Debe utilizar esta función para extraer variables.
# Esta función toma una expresión como entrada y devuelve una lista ordenada de variables.
# NO modifique esta función.

def extract_variables(expression):
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set


# ********************** FIN *******************************



############## IMPLEMENTAR LAS SIGUIENTES FUNCIONES  ##############
############## No modificar las definiciones de las funciones ##############

# Función: tabla_verdad
# Esta función calcula una tabla de verdad para una expresión dada.
# Entrada: expresión.
# Salida: tabla de verdad como una lista de listas.

def tabla_verdad(expr):
    var = extract_variables(expr)
    n_var = len(var)
    combinaciones = 2 ** n_var
    tabla_de_verdad = []

    for i in range(combinaciones):
        filas = []
        for val in range(n_var):
            valor = (i >> (n_var - 1 - val)) & 1
            filas.append(valor == 1)

        asignaciones = dict(zip(var, filas))
        asignaciones.update({"implies": implies, "iff": iff})

        try:
            resultado = eval(expr, {"__builtins__": None}, asignaciones)
            
        except Exception:
            resultado = False

        tabla_de_verdad.append(filas + [resultado])

    return tabla_de_verdad

# Función: tautologia
# Esta función determina si la expresión es una tautología, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión.
# Salida: booleano.
def tautologia(expr):
    variables = extract_variables(expr) # Variables atómicas
    
    n = len(variables)

    for i in range(2 ** n):  
        valores = {} # Declaracion del diccionario para evaluar con eval
        for j in range(n): # Itera en las variables (n es cantidad de variables)
            valores[variables[j]] = bool((i >> (n - j - 1)) & 1) # obtener el valor booleano de cada variable en la fila (i)

        
        try:
            resultado = eval(expr, {}, {**valores, "implies": implies, "iff": iff}) # Evalua la fila con los valores booleanos
        except Exception:
            return False  

        if resultado is not True: # Si alguno no es true, ya se sabe que es tautología
            return False  

    return True

#funcion valid sintaxis para el main... tal vez 

# Función: equivalentes
# Esta función determina si expr1 es equivalente a expr2, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión 1 y expresión 2.
# Salida: booleano.
def equivalentes(expr1, expr2):
    # 2 Expresiones son equivalentes si su doble inferencia es tautología
    variables1 = extract_variables(expr1)
    variables2 = extract_variables(expr2)
    
    if variables1 != variables2:
        return False
    
    expr3 = "(" + expr1 + ")" + " |iff| " + "(" + expr2 + ")"
    
    print(expr3)
    
    return tautologia(expr3)

# Función: inferencia
# Esta función determina los valores de verdad para una valuación de una proposición dada.
# Entrada: expresión.
# Salida: lista de listas.

def inferencia(expr):
    partes = expr.split('=')
    if len(partes) != 2: # Validar el formato
        return []
    proposicion = partes[0].strip() # Extraer proposición
    valor = partes[1].strip() # Extraer valor
    if valor == '1': #Expresión es igual a verdadera
        igual = True
    elif valor == '0': #Expresión es igual a falsa
        igual = False
    else:
        return []

    # Extraer variables y ordenarlas
    variables = extract_variables(proposicion)
    n = len(variables) #Número de variables
    resultados = [] #Lista para almacenar resultados

    # Generar todas las combinaciones posibles de valores de verdad
    for i in range(2 ** n):
        fila = [] #Fila para almacenar valores de verdad
        valores = {} #Diccionario para almacenar valores de verdad
        for j in range(n): #Recorrer las variables
            valor_bool = bool((i >> (n - j - 1)) & 1) #Obtener el valor de verdad
            fila.append(valor_bool) #Agregar valor a la fila
            valores[variables[j]] = valor_bool #Agregar valor al diccionario
        try: #Evaluar la proposición con los valores de verdad
            resultado = eval(proposicion, {}, {**valores, "implies": implies, "iff": iff}) #Evaluar la proposición
        except Exception: # Si hay un error en la evaluación, continuar con la siguiente iteración
            continue
        if resultado == igual: #Verificar si el resultado es igual al valor esperado
            resultados.append(fila) #Agregar fila a los resultados
    return resultados #Retornar resultados

print(inferencia('a and not a = 1'))
print(inferencia('(a and b) |implies| (c or not a) = 0'))
# Diego Equivalencia 
print(equivalentes("not (a and b)", "not a and not b"))
print(equivalentes("p |implies| q", "not p or q"))