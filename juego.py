import pygame
from constantes import *
import random
from funciones import *


pygame.init() # Inicializa el proyecto

carta_pregunta = {"superficie":pygame.Surface(TAMAÑO_PREGUNTA),"rectangulo":pygame.Rect((0,0,0,0))}
carta_pregunta['superficie'].fill(COLOR_GRIS)
#carta_pregunta = pygame.image.load("pregunta_1.png")
#carta_pregunta = pygame.transform.scale(carta_pregunta,TAMAÑO_PREGUNTA)
#carta_pregunta['superficie'].fill(COLOR_CELESTE)

un_segundo = pygame.USEREVENT
pygame.time.set_timer(un_segundo,1000)
cuadro_vidas = {"superficie":pygame.Surface(TAMAÑO_CUADRO),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_vidas['superficie'].fill(COLOR_ROJO)
cuadro_tiempo = {"superficie":pygame.Surface(TAMAÑO_CUADRO),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_tiempo['superficie'].fill(COLOR_GRIS)


cartas_respuestas = [
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))},#R1 -> 0
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))},#R2 -> 1
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))}#R3 -> 2
]

for carta in cartas_respuestas:
    carta['superficie'].fill(COLOR_DORADO)

# Definir texto de la pregunta
fuente_pregunta = pygame.font.SysFont("Arial Black",18)
fuente_respuesta = pygame.font.SysFont("Arial Rounded MT Bold",25)
fuente_puntuacion = pygame.font.SysFont("Arial Black",15)
fuente_vidas = pygame.font.SysFont("Arial Black",15)
fuente_tiempo = pygame.font.SysFont("Arial Black",15)

puntuacion = 0
random.shuffle(lista_preguntas)
indice_pregunta = 0

click_sonido = pygame.mixer.Sound("sonidos/correcta.mp3")
click_sonido.set_volume(1)


error_sonido = pygame.mixer.Sound("sonidos/error.mp3")
error_sonido.set_volume(1)

vidas_actuales = CANTIDAD_OPORTUNIDADES
segundos = 0
minutos = MINUTOS

def mostrar_juego(pantalla:pygame.Surface, eventos):
    global indice_pregunta
    global puntuacion 
    global vidas_actuales
    global minutos
    global segundos

    retorno = "juego"
    pregunta = lista_preguntas[indice_pregunta]

    for evento in eventos:
        # Si inicia la partida, inicializa la puntuacion en 0
        if vidas_actuales == CANTIDAD_OPORTUNIDADES and minutos == MINUTOS and segundos == 0:
            puntuacion = 0
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == un_segundo:
            cuadro_tiempo['superficie'].fill((COLOR_GRIS))
            if segundos == 0:
                if minutos == 0:
                    # Se acabó el tiempo, perder una vida
                    vidas_actuales -= 1
                    cuadro_vidas['superficie'].fill(COLOR_ROJO)
                    if vidas_actuales == 0:
                        #Resetear el tiempo y vidas para el siguiente juego
                        vidas_actuales = CANTIDAD_OPORTUNIDADES
                        minutos = MINUTOS
                        segundos = 0
                        retorno = "terminado"
                    #else:
                        # Resetear el tiempo para la siguiente pregunta
                        # minutos = 2
                        # segundos = 0
                else:
                    minutos -= 1
                    segundos = 59
            else:
                segundos -= 1
        if evento.type == pygame.MOUSEBUTTONDOWN:
        
            for i in range(len(cartas_respuestas)):
                if cartas_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                    if int(pregunta['correcta']) == (i + 1):
                        click_sonido.play()
                        print("RESPUESTA CORRECTA")
                        #Integracion Estadisticas
                        generar_estadistica(pregunta,lista_preguntas,True)              
                        carta_pregunta['superficie'].fill((COLOR_GRIS))
                        for carta in cartas_respuestas:
                            carta['superficie'].fill(COLOR_DORADO)

                        indice_pregunta += 1    

                        if indice_pregunta != len(lista_preguntas):
                            pregunta = lista_preguntas[indice_pregunta]
                        else:
                            # Termino el juego
                            indice_pregunta = 0
                            random.shuffle(lista_preguntas)
                            pregunta = lista_preguntas[indice_pregunta]

                        puntuacion += 100
                        # Resetear el tiempo para la siguiente pregunta
                        # minutos = 2
                        # segundos = 0
                    else:
                        print("RESPUESTA INCORRECTA")
                        #Integracion Estadisticas
                        generar_estadistica(pregunta,lista_preguntas,False)
                        error_sonido.play()

                        carta_pregunta['superficie'].fill((COLOR_GRIS))
                        for carta in cartas_respuestas:
                            carta['superficie'].fill(COLOR_DORADO)

                        indice_pregunta += 1
                        vidas_actuales -= 1
                        cuadro_vidas['superficie'].fill((COLOR_ROJO)) 
                        if vidas_actuales == 0:
                            #Resetear el tiempo y vidas para el siguiente juego
                            vidas_actuales = CANTIDAD_OPORTUNIDADES
                            minutos = MINUTOS
                            segundos = 0
                            retorno = "terminado"

                        if indice_pregunta != len(lista_preguntas):
                            pregunta = lista_preguntas[indice_pregunta]
                        else:
                            # Termino el juego
                            indice_pregunta = 0
                            random.shuffle(lista_preguntas)
                            pregunta = lista_preguntas[indice_pregunta]

                        puntuacion -= 50
                        # Resetear el tiempo para la siguiente pregunta
                        # minutos = 2
                        # segundos = 0

    imagen_juego = pygame.image.load("imagenes/imagen_1.png")
    imagen_juego = pygame.transform.scale(imagen_juego,(340,170))
    pantalla.fill(COLOR_NEGRO)
    pantalla.blit(imagen_juego,(90,58))
    # Carta pregunta
    pantalla.blit(carta_pregunta['superficie'], (90, 228))
    blit_text(carta_pregunta['superficie'], pregunta['pregunta'], (10, 10), fuente_pregunta)
    # Cuadro Vidas
    pantalla.blit(cuadro_vidas['superficie'], (380, 10))
    blit_text(cuadro_vidas['superficie'], f"VIDAS: {vidas_actuales}", (10, 20), fuente_vidas, COLOR_BLANCO)
    # Cuadro tiempo
    pantalla.blit(cuadro_tiempo['superficie'], (210, 10))
    blit_text(cuadro_tiempo['superficie'], f"TIEMPO      {minutos}:{segundos}", (21, 5), fuente_tiempo, COLOR_BLANCO)
    # Cartas respuestas
    cartas_respuestas[0]['rectangulo'] = pantalla.blit(cartas_respuestas[0]['superficie'], (125, 325))
    blit_text(cartas_respuestas[0]['superficie'], pregunta['respuesta_1'], (20, 15), fuente_respuesta, COLOR_BLANCO)

    cartas_respuestas[1]['rectangulo'] = pantalla.blit(cartas_respuestas[1]['superficie'], (125, 382))
    blit_text(cartas_respuestas[1]['superficie'], pregunta['respuesta_2'], (20, 15), fuente_respuesta, COLOR_BLANCO)

    cartas_respuestas[2]['rectangulo'] = pantalla.blit(cartas_respuestas[2]['superficie'], (125, 440))
    blit_text(cartas_respuestas[2]['superficie'], pregunta['respuesta_3'], (20, 15), fuente_respuesta, COLOR_BLANCO)

    # Mostrar puntuación
    blit_text(pantalla, f"Puntuación: {puntuacion} puntos", (10, 30), fuente_puntuacion, COLOR_CELESTE)
    
    return retorno