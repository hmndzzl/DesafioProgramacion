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


def expr_transformada(expr):
    pattern_implies = re.compile(r'(\([^\)]+\)|[a-z])\s*\|implies\|\s*(\([^\)]+\)|[a-z])')
    while pattern_implies.search(expr):
        expr = pattern_implies.sub(r'implies(\1, \2)', expr)

    pattern_iff = re.compile(r'(\([^\)]+\)|[a-z])\s*\|iff\|\s*(\([^\)]+\)|[a-z])')
    while pattern_iff.search(expr):
        expr = pattern_iff.sub(r'iff(\1, \2)', expr)

    return expr


# Función: tabla_verdad
# Esta función calcula una tabla de verdad para una expresión dada.
# Entrada: expresión.
# Salida: tabla de verdad como una lista de listas.

def tabla_verdad(expr):
    var = extract_variables(expr) # se llama a la funcion auxiliar para extraer las variables
    n_var = len(var) # se guarda el numero de variables
    combinaciones = 2 ** n_var # se calcula el numero de filas posibles (2^n)
    tabla_de_verdad = [] # se crea una lista para guardar las filas de la tabla
    
    expr_eval = expr_transformada(expr)  # Transformamos la expresión una sola vez antes del ciclo

    # se itera por cada una de las filas o combinaciones creadas
    for i in range(combinaciones):
        filas = [] # se crea una lista para guardar los valores de verdad

        # se itera por cada una de las variables
        for val in range(n_var):
            valor = (i >> (n_var - 1 - val)) & 1 #se obtiene el valor de la variable en la combinacion actual mediante un AND
            filas.append(valor == 1)

        # se crea un diccionario con las variables y sus valores de verdad
        asignaciones = dict(zip(var, filas))
        asignaciones.update({"implies": implies, "iff": iff}) # se actualiza el diccionario con las funciones de implicación y equivalencia

        # se evalua la expresion con eval con la expresion un diccionario de "globales" y el diccionario local
        try:
            resultado = eval(expr_eval, {"__builtins__": None}, asignaciones)

        # se maneja cualquier error que pueda ocurrir durante la evaluación
        except Exception:
            resultado = False

        # se agrega la fila con los valores de verdad y el resultado de la evaluacion a la tabla de verdad
        tabla_de_verdad.append(filas + [resultado])

    # devuelve la lista de listas
    return tabla_de_verdad

# Función: tautologia
# Esta función determina si la expresión es una tautología, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión.
# Salida: booleano.
def tautologia(expr):
    variables = extract_variables(expr) # Variables atómicas
    expr_eval = expr_transformada(expr)
    
    n = len(variables)

    for i in range(2 ** n):  
        valores = {} # Declaracion del diccionario para evaluar con eval
        for j in range(n): # Itera en las variables (n es cantidad de variables)
            valores[variables[j]] = bool((i >> (n - j - 1)) & 1) # obtener el valor booleano de cada variable en la fila (i)

        
        try:
            resultado = eval(expr_eval, {}, {**valores, "implies": implies, "iff": iff}) # Evalua la fila con los valores booleanos
        except Exception:
            return False  

        if resultado is not True: # Si alguno no es true, ya se sabe que es tautología
            return False  

    return True

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
    expr3_eval = expr_transformada(expr3)
    return tautologia(expr3_eval)

    

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
            propos_eval = expr_transformada(proposicion)
            resultado = eval(propos_eval, {}, {**valores, "implies": implies, "iff": iff})
        except Exception: # Si hay un error en la evaluación, continuar con la siguiente iteración
            continue
        if resultado == igual: #Verificar si el resultado es igual al valor esperado
            resultados.append(fila) #Agregar fila a los resultados
    return resultados #Retornar resultados


# Función propia para validar la sintaxis de una expresión
def sintaxis_valida(expr):
    try:
        expr_eval = expr_transformada(expr)
        entorno = {
            "implies": implies,
            "iff": iff,
            "and": lambda a, b: a and b,
            "or": lambda a, b: a or b,
            "not": lambda a: not a,
        }
        eval(expr_eval, {}, entorno)
        return True
    except (SyntaxError, NameError, TypeError, AttributeError):
        return False



#print(inferencia('a and not a = 1'))
#print(inferencia('(a and b) |implies| (c or not a) = 0'))
#print(equivalentes("not (a and b)", "not a and not b"))
#print(equivalentes("p |implies| q", "not p or q"))

#Menu
opcion = ""
while opcion != "5":
    print("\n===== MENÚ DE LÓGICA PROPOSICIONAL =====")
    print("1. Mostrar tabla de verdad")
    print("2. Verificar si una expresión es tautología")
    print("3. Verificar si dos expresiones son equivalentes")
    print("4. Realizar inferencia (proposición = 0 o 1)")
    print("5. Salir")
    opcion = input("Seleccione una opción (1-5): ").strip()

    if opcion == "1":
        expr = input("Ingrese expresión lógica para tabla de verdad: ").strip()
        if not sintaxis_valida(expr):
            print("Error: sintaxis inválida. Intente de nuevo.")
            continue
        tabla = tabla_verdad(expr)
        vars_ = extract_variables(expr)
        encabezado = " | ".join(vars_) + " | " + expr
        print("\n" + encabezado)
        print("-" * len(encabezado))
        for fila in tabla:
            valores = ["1" if val else "0" for val in fila[:-1]]
            res = "1" if fila[-1] else "0"
            print(" | ".join(valores) + " | " + res)

    elif opcion == "2":
        expr = input("Ingrese expresión lógica para verificar tautología: ").strip()
        if not sintaxis_valida(expr):
            print("Error: sintaxis inválida. Intente de nuevo.")
            continue
        es_tauto = tautologia(expr)
        print("La expresión **sí** es una tautología." if es_tauto else "La expresión **no** es una tautología.")

    elif opcion == "3":
        expr1 = input("Ingrese primera expresión: ").strip()
        expr2 = input("Ingrese segunda expresión: ").strip()
        if not sintaxis_valida(expr1) or not sintaxis_valida(expr2):
            print("Error: una o ambas expresiones tienen sintaxis inválida. Intente de nuevo.")
            continue
        son_eq = equivalentes(expr1, expr2)
        print("Las expresiones **sí** son equivalentes." if son_eq else "Las expresiones **no** son equivalentes.")

    elif opcion == "4":
        entrada = input("Ingrese proposición con valor esperado (ejemplo: «a and b = 1» o «p = 0»): ").strip()
        partes = entrada.split("=")
        if len(partes) != 2 or partes[0].strip() == "" or partes[1].strip() not in ("0", "1"):
            print("Error: formato inválido. Use «proposición = 0» o «proposición = 1».")
            continue
        propos = partes[0].strip()
        if not sintaxis_valida(propos):
            print("Error: sintaxis inválida en la proposición. Intente de nuevo.")
            continue
        resultados = inferencia(entrada)
        if not resultados:
            print("No se encontraron valuaciones que cumplan con esa inferencia.")
        else:
            vars_inf = extract_variables(propos)
            encabezado = " | ".join(vars_inf)
            print("\nValuaciones que hacen que la proposición sea igual a " + partes[1].strip() + ":")
            print(encabezado)
            print("-" * len(encabezado))
            for fila in resultados:
                print(" | ".join("1" if val else "0" for val in fila))

    elif opcion == "5":
        print("Saliendo.")

    else:
        print("Opción inválida. Por favor seleccione una opción del 1 al 5.")
