from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import barcos as b
import estadisticas as e

# Crear la aplicación
app = FastAPI(title="Hundir la flota", version="1.0.0")
juegos = {}  # Diccionario para almacenar tableros por game_id

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensaje": "Hundir la flota!"}

@app.get("/createGame/{game_id}/{PoX}/{PoY}/{nom}/{dificultad}")
def crear_juego(game_id: str, PoX: int, PoY: int, nom: str, dificultad: str):
    # Crear nuevo tablero para este game_id
    mi_taulell = b.taulell(PoX, PoY)
    mi_taulell.registrarNom(nom)
    resultado = mi_taulell.crear_matriz(PoX, PoY)
    if isinstance(resultado, str):
        return {"error": resultado}
    mi_taulell.generar_barcos_auto()
    juegos[game_id] = mi_taulell  # Almacenar tablero
    return {
        "game_id": game_id,
        "matrix": resultado,
        "barcos": [
            {
                "tamaño": barco.tamaño,
                "coordenadas": barco.cords
            }
            for barco in mi_taulell.lista_barcos
        ],
        "status": "created successfully",
        "size": {"rows": PoX, "cols": PoY}
    }

"""@app.get("/createShipSmall/{game_id}")
def crear_barcoS(game_id: str):
    if game_id not in juegos:
        return {"error": "Juego no encontrado"}
    mi_taulell = juegos[game_id]
    nuevo_barco = b.barcos(1, mi_taulell)
    resultado = nuevo_barco.crear_barcoPequeño()
    if isinstance(resultado, str):
        return {"error": resultado}
    return {
        "game_id": game_id,
        "barco": resultado,
        "status": "created successfully"
    }

@app.get("/createShipBig/{game_id}/{medida}")
def crear_barcoB(game_id: str, medida: int):
    if game_id not in juegos:
        return {"error": "Juego no encontrado"}
    mi_taulell = juegos[game_id]
    nuevo_barco = b.barcos(medida, mi_taulell)
    resultado = nuevo_barco.crear_barcoGrande(medida)
    if isinstance(resultado, str):
        return {"error": resultado}
    return {
        "game_id": game_id,
        "barco": resultado,
        "status": "created successfully"
    }"""

@app.get("/shot/{game_id}/{PoX}/{PoY}")
def crear_disparo(game_id: str, PoX: int, PoY: int):
    if game_id not in juegos:
        return {"error": "Juego no encontrado"}
    mi_taulell = juegos[game_id]
    if mi_taulell.lista_barcos:
        resultado = mi_taulell.lista_barcos[0].disparo(PoX, PoY)
    else:
        resultado = {"error": "No hay barcos creados"}
    return {
        "game_id": game_id,
        "resultado del disparo": resultado,
        "status": "created successfully"
    }

@app.get("/abandonar/{game_id}")
def abandonar(game_id: str):
    if game_id not in juegos:
        return {"error": "Juego no encontrado"}
    mi_taulell = juegos[game_id]
    mi_taulell.cleanPartida() 
    del juegos[game_id]  
    return {
        "game_id": game_id,
        "message": "Partida eliminada correctamente",
        "status": "yets"
    }



@app.get("/game/{game_id}/")
def juego(game_id: str):
    if game_id not in juegos:
        return {"error": "Juego no encontrado"}
    mi_taulell = juegos[game_id]
    resultado = mi_taulell.mostrar_partida()
    return {
        "game_id": game_id,
        "partida": resultado,
        "status": "created successfully"
    }

@app.get("/stats/{game_id}/{nom}")
def stats(game_id: str, nom: str):
    return e.obtener_stats()