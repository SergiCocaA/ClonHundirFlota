console.log("Frontend iniciado");

// Variables 
let disparos = 0;
let disparosFallados = 0;
let hundidos = 0;
let puntos = 0;

// Funcion 1: Generar ID de partida
function generarIdPartida() {
    return crypto.randomUUID();
}
let idPartida = localStorage.getItem("idPartida");
// Si no existe, lo creamos y guardamos
if (!idPartida) {
    idPartida = generarIdPartida();
    localStorage.setItem("idPartida", idPartida);
}

console.log("ID: ", idPartida);

// Funcion 2: Validar
function validarDimensiones(filas, columnas, nombre) {
    if (columnas > 20 || columnas < 7 || filas > 20 || filas < 7) {
        alert("Numero de filas o columnas invalido recuerda introducir del 7 a 20")
        return false
    } else if (nombre === "Anonimo") {
        alert("Introduce nombre !!!")
        return false
    } else {
        return true

    }
}

// Funcion 3: Generar la tabla 
function generarTabla(filas, columnas) {
    let celdas = ""
    for (let i = 0; i < filas; i++) {
        celdas += "<tr>"
        for (let j = 0; j < columnas; j++) {
            celdas += "<td id=" + i + j + ">💧​</td>"
        }
        celdas += "</tr>"
    }
    document.getElementById("tabla").innerHTML = celdas
}
// Funcion 4: Abandonar 
async function abandonarPartida() {
    // Fetch
    fetch(`http://127.0.0.1:8000/abandonar/${idPartida}`)
        .then(response => response.json())
        .then(data => {
            console.log("Partida abandonada :", data)
        })
        .catch(error => {
            console.error("Error: ", error)
        });
    document.getElementById("bloc2").style.display = "none"
    document.getElementById("bloc1").style.display = "none"
    document.getElementById("final").style.color = "red"
    document.getElementById("final").textContent = "DERROTA"
    document.getElementById("bloc3").style.width = "100%"
    document.getElementById('bloc3').style.display = 'block'

}
//Funcion 5: Reiniciar
function reiniciarPartida() {
    location.reload()
}
//Funcion 6: mostrar estadistias
function mostrarEstats() {
    document.getElementById("estadisticas").style.display = `block`
    fetch(`http://127.0.0.1:8000/stats/${idPartida}/${nombre}/`)
        .then(response => response.json())
        .then(data => {
            console.log("Listado", data)
            let mejoPuntuacion = data.mejor_puntuacion
            let mejorJugador = data.mejor_jugador
            let totalPartidas = data.total_partidas
            let top5 = data.top5

            if (top5 && top5.length >= 5) {
                let jugador1 = top5[0].jugador
                let puntuacion1 = top5[0].puntuacion
                let filas1 = top5[0].filas
                let columnas1 = top5[0].columnas

                let jugador2 = top5[1].jugador
                let puntuacion2 = top5[1].puntuacion
                let filas2 = top5[1].filas
                let columnas2 = top5[1].columnas

                let jugador3 = top5[2].jugador
                let puntuacion3 = top5[2].puntuacion
                let filas3 = top5[2].filas
                let columnas3 = top5[2].columnas

                let jugador4 = top5[3].jugador
                let puntuacion4 = top5[3].puntuacion
                let filas4 = top5[3].filas
                let columnas4 = top5[3].columnas

                let jugador5 = top5[4].jugador
                let puntuacion5 = top5[4].puntuacion
                let filas5 = top5[4].filas
                let columnas5 = top5[4].columnas

                document.getElementById("mejorPuntuacion").textContent = mejoPuntuacion
                document.getElementById("mejorJugador").textContent = mejorJugador
                document.getElementById("totalPartidas").textContent = totalPartidas

                document.getElementById("jugador0").textContent = jugador1
                document.getElementById("puntuacion0").textContent = puntuacion1
                document.getElementById("filas0").textContent = filas1
                document.getElementById("columnas0").textContent = columnas1

                document.getElementById("jugador1").textContent = jugador2
                document.getElementById("puntuacion1").textContent = puntuacion2
                document.getElementById("filas1").textContent = filas2
                document.getElementById("columnas1").textContent = columnas2

                document.getElementById("jugador2").textContent = jugador3
                document.getElementById("puntuacion2").textContent = puntuacion3
                document.getElementById("filas2").textContent = filas3
                document.getElementById("columnas2").textContent = columnas3

                document.getElementById("jugador3").textContent = jugador4
                document.getElementById("puntuacion3").textContent = puntuacion4
                document.getElementById("filas3").textContent = filas4
                document.getElementById("columnas3").textContent = columnas4

                document.getElementById("jugador4").textContent = jugador5
                document.getElementById("puntuacion4").textContent = puntuacion5
                document.getElementById("filas4").textContent = filas5
                document.getElementById("columnas4").textContent = columnas5
            } else {
                console.log("Data no es array válido o vacío");
            }

        })
        .catch(error => { console.error("Error al enviar datos:", error); })
}
// ¡¡¡PRINCIPAL!!!
let boton = document.getElementById('datos')
boton.addEventListener('click', function (event) {
    console.log('Click en datos')

    let filas = document.getElementById('filas').value
    let columnas = document.getElementById('columnas').value
    let nombre = document.getElementById('nombre').value.trim() || 'Anonimo'
    console.log("nombre " + nombre + " filas " + filas + " columnas " + columnas)

    // Validar
    if (!validarDimensiones(filas, columnas, nombre)) {
        return;
    }

    // jugador
    document.getElementById(`jugador`).textContent = `Jugador: ` + nombre
    // Generar tabla 
    generarTabla(filas, columnas)

    // Dificultad
    let Dfacil = document.getElementById(`facil`)
    let Dmedio = document.getElementById(`medio`)
    let Ddificil = document.getElementById(`dificil`)

    let dificultadTexto = ""
    if (Dfacil.checked) {
        dificultadTexto = "Fácil"
        console.log(`dificultad establecida facil`)
    } else if (Dmedio.checked) {
        dificultadTexto = "Media"
        console.log(`dificultad establecida media`)
    } else if (Ddificil.checked) {
        dificultadTexto = "Difícil"
        console.log(`dificultad establecida dificil`)
    } else {
        alert(`Selecciona dificultad`)
        return
    }
    document.getElementById(`textoDificultad`).textContent = dificultadTexto

    // Crear partida 
    fetch(`http://127.0.0.1:8000/createGame/${idPartida}/${filas}/${columnas}/${nombre}/${dificultadTexto}`)
        .then(response => response.json())
        .then(data => { console.log("Listado", data); })
        .catch(error => { console.error("Error al enviar datos:", error); })


    // Mostrar bloques 2 3
    document.getElementById('bloc2').style.display = 'block'
    document.getElementById('bloc3').style.display = 'block'



    // Configurar disparos
    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            document.getElementById(i + '' + j).addEventListener('click', function (event) {
                let fila = i
                let col = j

                // revisar si ha disparado
                if (event.target.classList.contains('tocado') || event.target.classList.contains('agua') || event.target.classList.contains('hundido')) {
                    return
                }

                // Fetch disparo
                fetch(`http://127.0.0.1:8000/shot/${idPartida}/${fila}/${col}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("Listado", data)
                        let resultado = data["resultado del disparo"].resultado
                        let puntosGanados = data["resultado del disparo"].puntos_ganados
                        let totalPuntos = data["resultado del disparo"].total_puntos
                        let estado = data["resultado del disparo"].estado

                        // resultado 
                        if (resultado === `agua`) {
                            event.target.classList.add(`agua`)
                            event.target.innerHTML = `🌊​`
                            disparosFallados++
                            document.getElementById(`disparosFallados`).textContent = `Disparos Fallados: ` + disparosFallados
                            document.getElementById(`ultimaJugada`).innerHTML = "<p>Últim mssatge: " + nombre + " ha tocat aigua en fila: " + fila + " columna: " + col + " ha perdut: " + puntosGanados + " punts</p>"
                            document.getElementById(`puntosGanados`).textContent = puntosGanados
                            document.getElementById(`puntosGanados`).style.color = `#ED2E14`
                        } else if (resultado === `tocado`) {
                            event.target.innerHTML = `​💣​`
                            event.target.classList.add(`tocado`)
                            disparos++
                            document.getElementById(`disparos`).textContent = "Disparos Acertados: " + disparos
                            document.getElementById(`ultimaJugada`).innerHTML = "<p>Últim mssatge: " + nombre + " ha tocat vaixell en fila: " + fila + " columna: " + col + " ha guanyat: +" + puntosGanados + " punts</p>"
                            document.getElementById(`puntosGanados`).textContent = `+` + puntosGanados
                            document.getElementById(`puntosGanados`).style.color = `#22CC2D`
                        } else if (resultado === `hundido`) {
                            event.target.classList.add(`hundido`)
                            event.target.innerHTML = `☠️​`
                            hundidos++
                            document.getElementById(`barcosHundidos`).textContent = "Barcos Hundidos: " + hundidos
                            document.getElementById(`ultimaJugada`).innerHTML = "<p>Últim mssatge: " + nombre + " ha enfonsat vaixell en fila: " + fila + " columna: " + col + " ha guanyat: +" + puntosGanados + " punts</p>"
                            document.getElementById(`puntosGanados`).textContent = `+ ` + puntosGanados
                            document.getElementById(`puntosGanados`).style.color = `#22CC2D`
                        }
                        document.getElementById(`puntos`).textContent = totalPuntos + ` Punts`

                        // Fin de juego
                        if (estado === 'Derrota') {
                            document.getElementById("bloc2").style.display = "none"
                            document.getElementById("bloc1").style.display = "none"
                            document.getElementById("final").style.color = "red"
                            document.getElementById("final").textContent = "DERROTA"
                            document.getElementById("bloc3").style.width = "100%"
                            document.getElementById("bloc23").style.width = "63%"
                            mostrarEstats()
                            document.getElementById("bloc23").classList.add("finalizado")
                            document.getElementById("imagenMario").style.display = "none"
                            console.log(`PERDEDOR`);
                        } else if (estado === 'Victoria') {
                            document.getElementById("bloc2").style.display = "none"
                            document.getElementById("bloc1").style.display = "none"
                            document.getElementById("bloc3").style.width = "100%"
                            document.getElementById("final").style.color = "green"
                            document.getElementById("final").textContent = "VICTORIA"
                            document.getElementById("bloc23").style.width = "63%"
                            console.log(`GANADOR`);
                            mostrarEstats()
                            document.getElementById("bloc23").classList.add("finalizado")

                        }

                        // Total disparos
                        let totalDisparos = disparos + disparosFallados;
                        document.getElementById(`totalDisparos`).textContent = totalDisparos
                    })
                    .catch(error => {
                        console.error("Error al enviar datos:", error)
                    })

                console.log('Click en ' + fila + ' y ' + col)
            })
        }
    }
})
//Configuracion de botones
//Abandonar
let botonAbandonar = document.getElementById('abandonar')
botonAbandonar.addEventListener('click', function (event) {
    abandonarPartida()
    console.log(`Abandono`)
})
//Reiniciar
let botonReiniciar = document.getElementById('reiniciar')
botonReiniciar.addEventListener('click', function (event) {
    console.log(`Reinicio`)
    reiniciarPartida();
})
//Avisar de si quiere recargar la pgina
window.onbeforeunload = function (event) {
    return "¿Quieres reiniciar la partida para intentarlo de nuevo?"
}
