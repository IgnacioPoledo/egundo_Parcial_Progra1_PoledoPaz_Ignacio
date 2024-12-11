import pygame
from funciones import *
from constantes import *
from opciones import *
from menu import *

pygame.init()
pantalla = pygame.display.set_mode((PANTALLA))
pygame.display.set_caption("THIS OR THAT")
fuente = pygame.font.Font(None, 36)

# Preguntas
banco_preguntas = [
    {"pregunta": "¿Preferis programar en Python o en JavaScript?", "opciones": ["Rojo", "Azul"], "valor": 100},
    {"pregunta": "¿Qué editor de código preferis VS Code o PyCharm?", "opciones": ["Rojo", "Azul"], "valor": 200},
    {"pregunta": "¿Preferis trabajar en frontend o backend?", "opciones": ["Rojo", "Azul"], "valor": 300},
    {"pregunta": "¿Preferis trabajar solo o en equipo?", "opciones": ["Rojo", "Azul"], "valor": 400},
    {"pregunta": "¿Preferis desarrollar o crear codigo?", "opciones": ["Rojo", "Azul"], "valor": 100}
]

# Estado del juego
estado_juego = {
    "jugador": {"nombre": "Jugador", "puntaje": 0, "vidas": 3},
    "preguntas_usadas": [],
}

def juego():
    
    estado_juego["jugador"]["vidas"] = 3
    estado_juego["jugador"]["puntaje"] = 0
    estado_juego["preguntas_usadas"] = []

    pregunta_actual = seleccionar_pregunta(banco_preguntas, estado_juego["preguntas_usadas"])
    votos = generar_votos()
    respuesta_correcta = determinar_ganador(votos)
    reloj = pygame.time.Clock()
    tiempo_restante = 60
    jugando = True

    rect_rojo = pygame.Rect(100, 200, 200, 50)
    rect_azul = pygame.Rect(500, 200, 200, 50)

    rect_next = pygame.Rect(150, 550, 150, 40)  
    rect_half = pygame.Rect(350, 550, 150, 40)  
    rect_reload = pygame.Rect(550, 550, 150, 40)  

    mostrar_colores = False
    
    # Indica si los comodines se usaron
    next_usado = False 
    half_usado = False  
    reload_usado = False 

    # Votantes
    votantes = []
    for i in range(11):
        x = 175 + (i % 6) * 98  # Posición horizontal
        y = 300 + (i // 6) * 150  # Posición vertical
        
        if i == 6:
            x,y = 215, 420
        elif i == 7:
            x,y = 315, 420
        elif i == 8:
            x,y = 415, 420
        elif i == 9:
            x,y = 515, 420
        elif i == 10:
            x,y = 615, 420

        votantes.append({"rect": pygame.Rect(x, y, 60, 60), "color": GRIS}) 

    while jugando:
        pantalla.fill(VERDE_AGUA)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
                break
            elif evento.type == pygame.USEREVENT:  # Evento del temporizador
                mostrar_colores = False  # Reiniciar bandera
                for votante in votantes:
                    votante["color"] = GRIS
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Desactivar el temporizador
            if evento.type == pygame.MOUSEBUTTONDOWN: 
                if rect_rojo.collidepoint(evento.pos):  #
                    if respuesta_correcta == "Rojo":
                        estado_juego["jugador"]["puntaje"] += pregunta_actual["valor"]
                        print("¡Respuesta correcta!")
                        mostrar_colores = True
                        pygame.time.set_timer(pygame.USEREVENT, 2000)
                        pregunta_actual = seleccionar_pregunta(banco_preguntas, estado_juego["preguntas_usadas"])
                        if not pregunta_actual:
                            print("¡No hay más preguntas!")
                            mostrar_victoria(pantalla, estado_juego["jugador"]["puntaje"])
                            jugando = False
                        else:
                            votos = generar_votos()
                            respuesta_correcta = determinar_ganador(votos)
                            # Reiniciar los colores de los votantes a gris
                            for votante in votantes:
                                votante["color"] = GRIS
                    else:
                        print("Respuesta incorrecta.")
                        estado_juego["jugador"]["vidas"] -= 1
                        mostrar_colores = False
                        if estado_juego["jugador"]["vidas"] <= 0:
                            print("¡Perdiste todas las vidas! Fin del juego.")
                            mostrar_derrota(pantalla, estado_juego["jugador"]["puntaje"])
                            jugando = False
                elif rect_azul.collidepoint(evento.pos):  # Si clic en el botón "Azul"
                    if respuesta_correcta == "Azul":
                        estado_juego["jugador"]["puntaje"] += pregunta_actual["valor"]
                        print("¡Respuesta correcta!")
                        mostrar_colores = True
                        pygame.time.set_timer(pygame.USEREVENT, 2000)
                        pregunta_actual = seleccionar_pregunta(banco_preguntas, estado_juego["preguntas_usadas"])
                        if not pregunta_actual:
                            print("¡No hay más preguntas!")
                            mostrar_victoria(pantalla, estado_juego["jugador"]["puntaje"])
                            jugando = False
                        else:
                            votos = generar_votos()
                            respuesta_correcta = determinar_ganador(votos)
                            # Reiniciar los colores de los votantes a gris
                            for votante in votantes:
                                votante["color"] = GRIS
                    else:
                        print("Respuesta incorrecta.")
                        estado_juego["jugador"]["vidas"] -= 1
                        mostrar_colores = False
                        if estado_juego["jugador"]["vidas"] <= 0:
                            print("¡Perdiste todas las vidas! Fin del juego.")
                            mostrar_derrota(pantalla, estado_juego["jugador"]["puntaje"])
                            jugando = False

                # Comodines
                elif rect_next.collidepoint(evento.pos) and not next_usado:
                    print("Comodín 'Next' usado.")
                    next_usado = True 
                    pregunta_actual = seleccionar_pregunta(banco_preguntas, estado_juego["preguntas_usadas"])
                    if not pregunta_actual:
                        print("¡No hay más preguntas!")
                        jugando = False
                    votos = generar_votos()
                    respuesta_correcta = determinar_ganador(votos)
                    # Reiniciar los colores de los votantes a gris
                    for votante in votantes:
                        votante["color"] = GRIS

                elif rect_half.collidepoint(evento.pos) and not half_usado: 
                    print("Comodín 'Half' usado.")
                    half_usado = True 
                    # Revelar el color de 2 votantes aleatorios
                    import random
                    indices_a_revelar = random.sample(range(len(votos)), 2)
                    for indice in indices_a_revelar:
                        print(f"Votante {indice + 1}: {votos[indice]}")

                elif rect_reload.collidepoint(evento.pos) and not reload_usado:  
                    print("Comodín 'Reload' usado.")
                    reload_usado = True 
                    pregunta_actual = seleccionar_pregunta(banco_preguntas, estado_juego["preguntas_usadas"])
                    votos = generar_votos()
                    respuesta_correcta = determinar_ganador(votos)
                    # Reiniciar los colores de los votantes a gris
                    for votante in votantes:
                        votante["color"] = GRIS

        # Dibujar los votantes
        for i, votante in enumerate(votantes):
            if mostrar_colores:  # Mostrar colores reales de los votantes
                votante["color"] = ROJO if votos[i] == "Rojo" else AZUL
            pygame.draw.rect(pantalla, votante["color"], votante["rect"])
            
        if pregunta_actual:
            mostrar_texto(pantalla, "Pregunta:", 98, 115, fuente)
            mostrar_texto(pantalla, pregunta_actual["pregunta"], 450, 150, fuente)

            pygame.draw.rect(pantalla, ROJO, (150, 200, 200, 50))
            mostrar_texto(pantalla, "Rojo", 250, 225, fuente, BLANCO, centrado=True)

            pygame.draw.rect(pantalla, AZUL, (550, 200, 200, 50))
            mostrar_texto(pantalla, "Azul", 650, 225, fuente, BLANCO, centrado=True)

        # Botones comodines
        pygame.draw.rect(pantalla, AMARILLO, rect_next)
        mostrar_texto(pantalla, "Next", rect_next.centerx, rect_next.centery, fuente, NEGRO, centrado=True)

        pygame.draw.rect(pantalla, AMARILLO, rect_half)
        mostrar_texto(pantalla, "Half", rect_half.centerx, rect_half.centery, fuente, NEGRO, centrado=True)

        pygame.draw.rect(pantalla, AMARILLO, rect_reload)
        mostrar_texto(pantalla, "Reload", rect_reload.centerx, rect_reload.centery, fuente, NEGRO, centrado=True)

        # Info del juego
        mostrar_texto(pantalla, f"Tiempo restante: {int(tiempo_restante)}", 700, 50, fuente)
        mostrar_texto(pantalla, f"Puntaje: {estado_juego['jugador']['puntaje']}", 100, 50, fuente)
        mostrar_texto(pantalla, f"Vidas: {estado_juego['jugador']['vidas']}", 400, 50, fuente)

        pygame.display.flip()

        reloj.tick(60)
        tiempo_restante -= 1 / 60
        if tiempo_restante <= 0:
            print("¡Se acabó el tiempo! Fin del juego.")
            jugando = False

# Musica 
try:
    pygame.mixer.music.load("Juego/sonidos/music_fondo.mp3")
    pygame.mixer.music.play(-1)  
    pygame.mixer.music.set_volume(volumen / 100)  
except pygame.error as e:
    print(f"Error al cargar la música: {e}")

# Main
if __name__ == "__main__":
    opcion = "menu" 
    while True:
        eventos = pygame.event.get()  
        if opcion == "menu":
            opcion = menu_principal(pantalla, fuente) 
        elif opcion == "jugar":
            juego()  
            opcion = "menu" 
        elif opcion == "opciones":
            retorno = mostrar_opciones(pantalla, eventos)  # Llamamos a mostrar_opciones
            pygame.display.flip()
            if retorno == "menu":
                opcion = "menu"  # Volvemos al menú
            elif retorno == "salir":
                break  # Salimos del juego
        elif opcion == "salir":
            break

    pygame.quit()
