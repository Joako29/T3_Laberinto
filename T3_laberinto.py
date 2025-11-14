import sys
# Aumentar el límite de recursión para laberintos grandes
sys.setrecursionlimit(2000)

# --- 1. Definición del Laberinto y Parámetros ---

# LABERINTO DE EJEMPLO 9x9 (Se necesita la matriz real para el resultado final)
# 0: Inicio (verde) o Fin (rojo) | >0: Gasta Energía | <0: Repone Energía | 99: Pared
LABERINTO_ORIGINAL = [
    [0, 1, 99, 1, 1, 1, 1, 1, 1], # (0, 0) es el Inicio
    [1, 1, 1, 1, -2, 1, 99, 1, 1],
    [1, 99, 1, 99, 1, 1, 99, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, -2],
    [99, 1, 99, 99, 1, 99, 1, 99, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 99, 1, 99, 99, 1, 99, 1, 1],
    [1, 1, 1, -2, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0] # (8, 8) es el Fin
]

N = 9 # Dimensión
ENERGIA_INICIAL = 18
INICIO_X, INICIO_Y = 0, 0
FIN_X, FIN_Y = 8, 8

# Prioridad de movimiento: Izquierda, Abajo, Arriba, Derecha
DIRECCIONES = [
    (0, -1),  # Izquierda
    (1, 0),   # Abajo
    (-1, 0),  # Arriba
    (0, 1)    # Derecha
]

# Matriz para almacenar la solución (1 = camino encontrado)
CAMINO_SOLUCION = [[0] * N for _ in range(N)]

# --- 2. Función de Impresión ---

def imprimir_matriz(matriz, titulo):
    """Muestra la matriz de forma legible."""
    print(f"\n{titulo}:")
    print("-" * (N * 5 + 3))
    for fila in matriz:
        # Se usa un formato condicional para visualizar mejor el camino
        linea = []
        for celda in fila:
            if celda == 1:
                linea.append(f"\033[92m {celda:2}\033[0m") # Verde para el camino
            elif celda == 99:
                linea.append(f"\033[91m {celda:2}\033[0m") # Rojo para paredes
            else:
                linea.append(f" {celda:2}")
        print(" | ".join(linea))
    print("-" * (N * 5 + 3))

# --- 3. Algoritmo de Backtracking con Restricción de Energía ---

def resolver_laberinto_backtracking(x, y, energia_restante):
    """
    Función recursiva de Backtracking para buscar la salida.

    :param x: Fila actual.
    :param y: Columna actual.
    :param energia_restante: Energía actual.
    :return: True si se encuentra un camino, False si no.
    """
    #  Caso Base 1: Éxito
    if x == FIN_X and y == FIN_Y:
        CAMINO_SOLUCION[x][y] = 1
        print(f"\n ¡Éxito! Camino encontrado. Energía final restante: {energia_restante} unidades.")
        return True

    # Marcar la celda actual como parte del camino temporal
    CAMINO_SOLUCION[x][y] = 1

    # Explorar las direcciones en el orden de prioridad: Izquierda, Abajo, Arriba, Derecha
    for dx, dy in DIRECCIONES:
        nx, ny = x + dx, y + dy

        # 1. Verificar límites de la matriz
        if 0 <= nx < N and 0 <= ny < N:

            valor_celda = LABERINTO_ORIGINAL[nx][ny]
            
            # 2. Verificar PARED (99)
            if valor_celda == 99:
                continue

            # 3. Calcular la nueva energía (Costo/Ganancia)
            # Las celdas 0 (Inicio/Fin) no alteran la energía
            if valor_celda == 0:
                nueva_energia = energia_restante
            else:
                # El costo es el valor de la celda (positivo gasta, negativo repone)
                nueva_energia = energia_restante - valor_celda
            
            # 4. Aplicar la RESTRICCIÓN DE PODA (Poda de nodos)
            # Si la energía baja de cero, este camino se poda.
            if nueva_energia < 0:
                continue
            
            # 5. Evitar ciclos y llamar recursivamente
            if CAMINO_SOLUCION[nx][ny] == 0: # Si la celda no ha sido visitada en esta rama
                if resolver_laberinto_backtracking(nx, ny, nueva_energia):
                    return True # Propagar el éxito

    #  Backtracking: Si ninguna dirección funcionó, desmarcar la celda
    CAMINO_SOLUCION[x][y] = 0
    return False

# --- 4. Ejecución ---

if __name__ == "__main__":
    imprimir_matriz(LABERINTO_ORIGINAL, " Laberinto ")
    
    # Inicia la búsqueda desde (0, 0) con 18 unidades de energía
    if resolver_laberinto_backtracking(INICIO_X, INICIO_Y, ENERGIA_INICIAL):
        imprimir_matriz(CAMINO_SOLUCION, " Camino Encontrado")
    else:
        print("\n ¡Fracaso! No se encontró ningún camino válido que mantenga la energía >= 0.")