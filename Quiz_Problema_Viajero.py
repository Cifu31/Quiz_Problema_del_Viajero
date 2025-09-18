# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 08:34:26 2025

@author: camic
"""

import random
import math

# Ciudades dadas con coordenadas
ciudades = {
    'A': (0, 0),
    'B': (1, 5),
    'C': (2, 3),
    'D': (5, 2),
    'E': (6, 6),
    'F': (7, 1),
    'G': (8, 4),
    'H': (9, 9)
}

# ---- Funciones auxiliares ----

def distancia(ciudad1, ciudad2):
    x1, y1 = ciudades[ciudad1]
    x2, y2 = ciudades[ciudad2]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distancia_ruta(ruta):
    """Calcular distancia total de una ruta (ida y regreso al inicio)."""
    total = 0
    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        siguiente = ruta[(i+1) % len(ruta)]  # regresar al inicio
        total += distancia(ciudad_actual, siguiente)
    return total

def crear_poblacion_inicial(tam_poblacion):
    """Crear población inicial de rutas aleatorias."""
    poblacion = []
    ciudades_lista = list(ciudades.keys())
    for _ in range(tam_poblacion):
        ruta = ciudades_lista[:]
        random.shuffle(ruta)
        poblacion.append(ruta)
    return poblacion

def seleccion(poblacion):
    """Selección por torneo (elige la mejor entre k al azar)."""
    k = 3
    candidatos = random.sample(poblacion, k)
    candidatos.sort(key=lambda r: distancia_ruta(r))
    return candidatos[0]

def cruce(padre1, padre2):
    """Cruce ordenado (OX)."""
    inicio, fin = sorted(random.sample(range(len(padre1)), 2))
    hijo = [None] * len(padre1)

    # Copiar segmento del padre1
    hijo[inicio:fin] = padre1[inicio:fin]

    # Rellenar con genes del padre2 en orden
    pos = fin
    for ciudad in padre2:
        if ciudad not in hijo:
            if pos >= len(hijo):
                pos = 0
            hijo[pos] = ciudad
            pos += 1
    return hijo

def mutacion(ruta, tasa_mutacion):
    """Mutación por intercambio."""
    for i in range(len(ruta)):
        if random.random() < tasa_mutacion:
            j = random.randint(0, len(ruta) - 1)
            ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

# ---- Algoritmo Genético Principal ----

def algoritmo_genetico(tam_poblacion=50, generaciones=200, tasa_mutacion=0.01):
    poblacion = crear_poblacion_inicial(tam_poblacion)
    mejor_ruta = min(poblacion, key=distancia_ruta)
    
    for gen in range(generaciones):
        nueva_poblacion = []
        for _ in range(tam_poblacion):
            padre1 = seleccion(poblacion)
            padre2 = seleccion(poblacion)
            hijo = cruce(padre1, padre2)
            hijo = mutacion(hijo, tasa_mutacion)
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
        mejor_gen = min(poblacion, key=distancia_ruta)
        if distancia_ruta(mejor_gen) < distancia_ruta(mejor_ruta):
            mejor_ruta = mejor_gen
        
        # Mostrar progreso
        if gen % 20 == 0:
            print(f"Generación {gen}: mejor distancia = {distancia_ruta(mejor_ruta):.2f}")
    
    return mejor_ruta, distancia_ruta(mejor_ruta)

# ---- Ejecutar ----
mejor, distancia_mejor = algoritmo_genetico()
print("\nMejor ruta encontrada:", mejor)
print("Distancia total:", round(distancia_mejor, 2))
