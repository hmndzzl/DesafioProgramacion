# DesafioProgramacion

Este programa implementa un sistema interactivo para trabajar con logica proposicional.
Este permite que: 
1. Mostrar la **tabla de verdad** de una proposición lógica.
2. Verificar si una proposición es una **tautología**.
3. Verificar si dos proposiciones son **equivalentes**.
4. Realizar **inferencias** para encontrar combinaciones que cumplan un valor esperado.

El programa permite:
- Variables proposicionales con letras minusculas. Ej ("a", "b", "c",...).
- Operadores lógicos: 
    - "and" conjuncion 
    - "or" disyunción
    - "not" negación
    - "|implies|" implicación
    - "|iff|" doble implicación
-Uso de parentesis para agrupar expresiones

## Ejecución
Para ejecutar el programa, abrir una terminal en la carpeta donde se encuentra el archivo y escribir:

```bash
python D1.py
```

Al iniciar se mostrara el menú:
===== MENÚ DE LÓGICA PROPOSICIONAL =====
1. Mostrar tabla de verdad
2. Verificar si una expresión es tautología
3. Verificar si dos expresiones son equivalentes
4. Realizar inferencia (proposición = 0 o 1)
5. Salir
Seleccione una opción (1-5):

## Restricciones 
- Las variables deben ser letras minúsculas. 
- No se debe escribir llamadas a funciones como "tautologia(...) en las entradas del menú. 
- El programa detectará errores de sintaxis y pedirá reintentar.
- Los operadores deben "|implies|" y "|iff|" deben escribirse exactamente así, con las barras verticales.


## Ejemplos de ejecución y formato de entrada 
1. Tabla de verdad 
Entrada: 
Seleccione una opción (1-5): 1
Ingrese expresión lógica para tabla de verdad: p and q

Salida: 
[[False, False, False],
 [False, True, False],
 [True, False, False],
 [True, True, True]]

2. Tautología
Entrada: 
Seleccione una opción (1-5): 2
Ingrese expresión lógica para verificar tautología: (a and b) |implies| a

Salida: 
True

3. Verificar equivalencia
Entrada: 
Seleccione una opción (1-5): 3
Ingrese primera expresión: not (a and b)
Ingrese segunda expresión: not a or not b

Salida: 
True

4. Inferencia
Entrada: 
Seleccione una opción (1-5): 4
Ingrese proposición con valor esperado (ejemplo: «a and b = 1» o «p = 0»): a or b = 0

Salida: 
[[False, False]]

## Nombres de los integrantes
Diego André Calderón Salazar - 241263
Pedro Julio Caso Tzunun - 241286
Hugo Roberto Méndez Lee - 241265
Ruth Daniela Ruano Orellana - 241098
