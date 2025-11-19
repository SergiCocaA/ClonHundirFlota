import random as rd
import estadisticas as e


# Clase taulell
class taulell:
    
    def __init__(self, filas, columnas):
        self.Filas = filas
        self.Columnas = columnas
        self.tabla = []
        self.lista_barcos = []
        self.puntuacion = 1000
        self.historial_disparos = []
        self.barcosHundidos = 0
        self.casillasMarcadas = 0
        self.casillasDerrota = 0
        self.nom = str

    # Añadir barcos desde la clase barcos
    def añadirlistabarco (self, barcos):
        self.lista_barcos.append(barcos)
    
    def registrarNom (self , nom):
        self.nom = nom 

    def comprobarBarcos (self):
        for barco in self.lista_barcos:
            if barco.cords:  # si tiene cords es q aun hay barcos
                return False
        return True
    
    # Crear la matriz y devolver mensaje si está mal
    def crear_matriz(self, filas, columnas):
        if filas < 7 or columnas < 7: 
            return "La matriz debe ser mayor a 7x7"
        else:  
            self.Filas = filas
            self.Columnas = columnas
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    fila.append("X")
                matriz.append(fila)
            self.tabla = matriz
            self.lista_barcos = []      
            self.historial_disparos = []  
            self.puntuacion = 1000  
            return self.tabla
    
    def cleanPartida(self):
        self.Filas = 0
        self.Columnas = 0
        self.tabla = []
        self.lista_barcos = []
        self.puntuacion = 1000
        self.historial_disparos = []

    
    def generar_barcos_auto(self):
        if not self.tabla:
            return "Matriz no creada"
        self.crear_barcosMinimos()

        totalMatriz = self.Filas * self.Columnas
        maxTamaño = int(totalMatriz * 0.30)  # Max 30% de las celdas
        celdasOcupadas = sum(barco.tamaño for barco in self.lista_barcos) #COntar barcos minimos 
        tamañoDisponible = [1, 2, 3, 4, 5]  
        max_intentos = 1000  #Creo esta variable de intentos para q no este siemple en un constante bucle y no se pete, es decir, un limite
        intentos = 0
        
        
        while celdasOcupadas < maxTamaño and intentos < max_intentos:
            
            tamaño = rd.choice(tamañoDisponible)  # Seleccionar tamaño aleatorio
            if celdasOcupadas + tamaño > maxTamaño:
                intentos += 1
                continue
            barco1 = barcos(tamaño, self)
            if tamaño == 1:
                resultado = barco1.crear_barcoPequeño()
            else:
                resultado = barco1.crear_barcoGrande(tamaño)
            if isinstance(resultado, str):  # Si hay error, intentar de nuevo
                intentos += 1
                continue
            celdasOcupadas += tamaño  # Actualizar celdas ocupadas
            intentos = 0  # Resetear intentos tras exito
            if intentos >= max_intentos:
                print("Deja de funcionar por bucle infinito MAX INTNETOS")

        celdas_libres = self.Filas * self.Columnas 
        self.casillasDerrota = (celdas_libres * 0.7) // 2
    
    
    
    # Verificar si ya hay algún barco con esas coordenadas
    def cords_ocupadas(self):
        ocupadas = set()# Lo paso a set para mejor rendimiento
        for barco in self.lista_barcos:
            ocupadas.update(barco.cords) 
        return ocupadas
    
    # Muestro la partida del jugador ID
    def mostrar_partida(self):
        return {
            "matriz": self.tabla,
            "barcos": [
                {
                    "tamaño": barco.tamaño,
                    "coordenadas": barco.cords,
                    "estado": "activo" if len(barco.cords) > 0 else "hundido"
                }
                for barco in self.lista_barcos
            ],
            "puntuacion": self.puntuacion,
            "historial_disparos": self.historial_disparos
        }
    
    #registrar los dipsaros y los puntos acorde a la palabra
    def registrar_disparo(self,resultado, PoX, PoY):
            puntos = 0
            if resultado == "agua":
                puntos = -10
            elif resultado == "tocado":
                puntos = +20
            elif resultado == "hundido":
                puntos = +50
            self.historial_disparos.append({
            "coordenadas": (PoX, PoY),
            "resultado": resultado,
            "puntos": puntos
            })
            if resultado == "agua":
                self.puntuacion -= 10
            elif resultado == "tocado":
                self.puntuacion += 20
            elif resultado == "hundido":
                self.puntuacion += 50 
                self.barcosHundidos += 1

    def registrar_casilla(self, resultado):
        if resultado == "agua":
            self.casillasMarcadas += 1
    
    
    def crear_barcosMinimos(self):
        if not self.tabla: #es para omprobar q este creada y no se cree x crear sin guardar en ningun sitio aleatorio
            return "Matriz no creada"
        
        tamaños = [1, 2, 3, 4, 5]
        max_intentos = 1000
        
        for mida in tamaños:
            intents = 0
            colocat = False
            while not colocat and intents < max_intentos:
                barco = barcos(mida, self)
                if mida == 1:
                    resultat = barco.crear_barcoPequeño()
                else:
                    resultat = barco.crear_barcoGrande(mida)
                if not isinstance(resultat, str):  # Si se a creado correactamente, es decir, si resultado es guardado como string es incorrecto, ya q es el error, es caso q no ponga if NOT significa q guardo el error y vuelve a probar
                    colocat = True
                intents += 1
            if not colocat:
                print("Maximo de intentos, intenta de nuevo")


# Clase barcos

class barcos:
    def __init__(self, tamaño, taulell = None  ):#pongo taulell q es none ya q si creo barco no podria acceder a los datos del taulell
        self.tamaño = tamaño
        self.cords = []
        self.taulell = taulell
    
    # compruebo si no me salgo de la matriz em todos los lados, si es el caso q en un lado funciona paso solamente ese
    def comprobar_direccion(self, PoX, PoY, direccion, tamaño):
        coords = []
        if direccion == 'X1':  # Horizontal derecha
            if PoX + (tamaño - 1) >= self.taulell.Filas:
                return []
            for i in range(tamaño):
                coords.append((PoX + i, PoY))
        elif direccion == "X2":   # Horizontal izquierda
            if PoX - (tamaño - 1) < 0:
                return []
            for i in range(tamaño):
                coords.append((PoX - i, PoY))
        elif direccion == 'Y2':  # Vertical abajo
            if PoY + (tamaño - 1) >= self.taulell.Columnas:
                return []
            for i in range(tamaño):
                coords.append((PoX, PoY + i))
        elif direccion == "Y1": # Vertical arriba
            if PoY - (tamaño - 1) < 0:
                return []
            for i in range(tamaño):
                coords.append((PoX, PoY - i))
        return coords
    
    
    
    # creo barco pequeño usando funcionas ya creadas para ayudarme
    def crear_barcoPequeño(self):
        salir = True
        while salir:
            PoX = rd.randint(0, self.taulell.Filas - 1)  
            PoY = rd.randint(0, self.taulell.Columnas - 1)
            
            if (PoX, PoY) in self.taulell.cords_ocupadas():  
                continue  # sigue buscando
            else:
                self.cords = [(PoX, PoY)]
                self.tamaño = 1
                self.taulell.añadirlistabarco(self) 
                salir = False
        
        return self.cords
    
    def crear_barcoGrande(self, tamaño):
        if tamaño > 5:
            return "Tamaño incorrecto"
        else:
            salir = True
            while salir:
                PoX = rd.randint(0, self.taulell.Filas - 1)
                PoY = rd.randint(0, self.taulell.Columnas - 1)
                
                direcciones = [
                    self.comprobar_direccion(PoX, PoY, "X1", tamaño),
                    self.comprobar_direccion(PoX, PoY, "X2", tamaño),
                    self.comprobar_direccion(PoX, PoY, "Y1", tamaño),
                    self.comprobar_direccion(PoX, PoY, "Y2", tamaño)
                ]
                rd.shuffle(direcciones)
                for coords in direcciones:
                    if len(coords) == tamaño:
                        ocupado = self.taulell.cords_ocupadas() 
                        if all(coord not in ocupado for coord in coords):
                            self.cords = coords
                            self.tamaño = tamaño
                            self.taulell.añadirlistabarco(self)
                            salir = False
                            break        
            return self.cords

    def disparo(self, PoX, PoY):        
        if PoX >= self.taulell.Filas or PoY >= self.taulell.Columnas or PoX < 0 or PoY < 0:
            return "Fuera de la tabla"
        else:
            barco_tocado = None # Cambiar de 0 a None ya q detecta 0 cada vez q lo busca en vez de las cords(basicamente es false)
            for barco in self.taulell.lista_barcos:
                if(PoX, PoY) in barco.cords:
                    barco_tocado = barco
                    break
            if barco_tocado == None:
                resultado = "agua"
                self.taulell.registrar_casilla(resultado)
                self.taulell.registrar_disparo(resultado, PoX, PoY)
                if (self.taulell.casillasMarcadas >= self.taulell.casillasDerrota and not self.taulell.comprobarBarcos()):
                    e.terminar_partida(self.taulell.nom, self.taulell.puntuacion, self.taulell.Filas, self.taulell.Columnas)
                    return{
                       "valor": "agua",
                        "resultado": resultado,
                        "coordenadas": (PoX, PoY),
                        "puntos_ganados": -10,
                        "estado": "Derrota",
                        "total_puntos": self.taulell.puntuacion 
                    }
                return {
                    "valor": "agua",
                    "resultado": resultado,
                    "coordenadas": (PoX, PoY),
                    "puntos_ganados": -10,
                    "estado": "En curso",
                    "total_puntos": self.taulell.puntuacion
                }  
            barco_tocado.cords.remove((PoX, PoY))
            if len(barco_tocado.cords) == 0:  
                resultado = "hundido"
                self.taulell.registrar_casilla(resultado)
                self.taulell.registrar_disparo(resultado, PoX, PoY)  
                if self.taulell.comprobarBarcos():
                    e.terminar_partida(self.taulell.nom, self.taulell.puntuacion, self.taulell.Filas, self.taulell.Columnas)
                    return{
                        "valor": "barco",
                        "resultado": resultado,
                        "coordenadas": (PoX, PoY),
                        "puntos_ganados": +50,
                        "estado": "Victoria",
                        "total_puntos": self.taulell.puntuacion
                    }
                return{
                    "valor": "barco",
                    "resultado": resultado,
                    "coordenadas": (PoX, PoY),
                    "puntos_ganados": +50,
                    "estado": "En curso",
                    "total_puntos": self.taulell.puntuacion
                } 
            else:
                resultado = "tocado"
                self.taulell.registrar_casilla(resultado)
                self.taulell.registrar_disparo(resultado, PoX, PoY)
                return {
                    "resultado": "tocado",
                    "coordenadas": (PoX, PoY),
                    "barco_tamaño": barco_tocado.tamaño,
                    "puntos_ganados": +20,
                    "estado": "En curso",
                    "total_puntos": self.taulell.puntuacion
                }
