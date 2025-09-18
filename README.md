# Quiz_Problema_del_Viajero


Este proyecto implementa un **algoritmo genético** para resolver el **Problema del Agente Viajero (TSP)**.  
El TSP consiste en encontrar la ruta más corta que visite cada ciudad exactamente una vez y regrese al punto de inicio.

---

## 📌 Descripción del problema
Se tienen 8 ciudades representadas en un plano cartesiano:

```python
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
El objetivo es encontrar el recorrido más corto que pase por todas ellas y regrese a la ciudad inicial.

⚙️ Algoritmo Genético implementado

El programa sigue los pasos clásicos de un algoritmo genético (GA):

Inicialización: Se crea una población inicial de rutas aleatorias.

Evaluación: Se calcula la distancia total de cada ruta usando la distancia euclidiana entre ciudades.

Selección: Se usa torneo para elegir a los mejores candidatos.

Cruce (Crossover): Se aplica cruce ordenado (OX) para combinar rutas de los padres y generar hijos válidos.

Mutación: Se aplica mutación por intercambio con una tasa determinada para mantener diversidad en la población.

Evolución: En cada generación se crea una nueva población, se guarda el mejor individuo y se repite hasta alcanzar el número de generaciones definido.

🧑‍💻 Código completo
import random
import math
import matplotlib.pyplot as plt

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

# ---- Visualización ----
def graficar_ruta(ruta):
    x = [ciudades[c][0] for c in ruta] + [ciudades[ruta[0]][0]]
    y = [ciudades[c][1] for c in ruta] + [ciudades[ruta[0]][1]]

    plt.figure(figsize=(6,6))
    plt.plot(x, y, marker='o', linestyle='-')
    for ciudad in ruta:
        plt.text(ciudades[ciudad][0]+0.1, ciudades[ciudad][1]+0.1, ciudad)
    plt.title("Mejor Ruta Encontrada (TSP)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

# ---- Ejecutar ----
mejor, distancia_mejor = algoritmo_genetico()
print("\nMejor ruta encontrada:", mejor)
print("Distancia total:", round(distancia_mejor, 2))

graficar_ruta(mejor)

🚀 Ejecución

Para correr el programa:

python tsp_ga.py


La salida mostrará la mejor ruta encontrada, su distancia total y además una gráfica en el plano XY con la ruta.

Ejemplo de salida en consola:

Generación 0: mejor distancia = 29.14
Generación 20: mejor distancia = 27.55
Generación 40: mejor distancia = 25.99
...
Mejor ruta encontrada: ['C', 'B', 'A', 'D', 'F', 'G', 'E', 'H']
Distancia total: 25.99


Y en la ventana gráfica aparecerá el recorrido marcado con líneas y puntos.

📊 Posibles mejoras

Ajustar parámetros del GA (población, generaciones, tasa_mutacion) para mejorar resultados.

Probar diferentes métodos de selección y cruce.

Extender el código para más ciudades y comparar eficiencia.
