import os
import json

# ruta 
CARPETA = "data"
FICHERO = "data/stats.json"

# crear la carpeta si no existe 
if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)

total_partidas = 0
mejor_puntuacion = 0
mejor_jugador = "ninguno"
top5 = []  

# si el fichero json existe se usa ese si no se crea uno de 0 con los parametros por defecto
if os.path.exists(FICHERO):
    try:
        with open(FICHERO) as ficheroAbrir:
            datos = json.load(ficheroAbrir)# guardo los datos del fichero en una variable
            total_partidas = datos["total_partidas"]
            mejor_puntuacion = datos["mejor_puntuacion"]
            mejor_jugador = datos["mejor_jugador"]
            top5 = datos["top5"]
    except:
        print("No hay ningun json creado, se usaran valroes x defecto")

# guardar los nuevos datos 
def guardar():
    datos = {
        "total_partidas": total_partidas,
        "mejor_puntuacion": mejor_puntuacion,
        "mejor_jugador": mejor_jugador,
        "top5": top5
    }
    with open(FICHERO, 'w') as ficheroAbrir: # q se abra modo lectura W
        json.dump(datos, ficheroAbrir)
    print("stats guardadas en data/stats.json")

# terminar partida
def terminar_partida(jugador, puntuacion, filas, columnas):
    global total_partidas, mejor_puntuacion, mejor_jugador, top5

    total_partidas += 1  

    # mejor puntuacion
    if puntuacion > mejor_puntuacion:
        mejor_puntuacion = puntuacion
        mejor_jugador = jugador

    top5.append({
        "jugador": jugador,
        "puntuacion": puntuacion,
        "filas": filas,
        "columnas": columnas
    })

    # key=lambda x: x["puntuacion"] → "ordena por el valor de 'puntuacion' de cada jugador"
    # Es como decir "no compares los nombres, compara solo los puntos"
    # reverse=True → pone el mas alto primero
    top5.sort(key=lambda x: x["puntuacion"], reverse=True)
    top5[:] = top5[:5]  

    guardar()  

# obtener stats 

def obtener_stats():
    return {
        "total_partidas": total_partidas,
        "mejor_puntuacion": mejor_puntuacion,
        "mejor_jugador": mejor_jugador,
        "top5": top5
    }
