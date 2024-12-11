import random
import pygame
from constantes import *

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# Función para seleccionar una pregunta
def seleccionar_pregunta(banco_preguntas, preguntas_usadas):
    preguntas_disponibles = [
        pregunta for pregunta in banco_preguntas if pregunta not in preguntas_usadas
    ]
    if not preguntas_disponibles:
        return None
    pregunta = random.choice(preguntas_disponibles)
    preguntas_usadas.append(pregunta)
    return pregunta

# Función para generar votos aleatorios
def generar_votos():
    return [random.choice(["Rojo", "Azul"]) for _ in range(11)]

# Función para determinar el ganador según los votos
def determinar_ganador(votos):
    rojo = votos.count("Rojo")
    azul = votos.count("Azul")
    return "Rojo" if rojo > azul else "Azul"

# Función para renderizar texto en pantalla
def mostrar_texto(pantalla, texto, x, y, fuente, color=(0, 0, 0), centrado=False):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y) if centrado else (x, y))
    pantalla.blit(superficie_texto, rect_texto)

def mostrar_victoria(pantalla, puntaje): 
    pantalla.fill(NEGRO) 
    mensaje = f"Ganaste! Tu puntaje es: {puntaje}" 
    fuente_felicitaciones = pygame.font.Font(None, 50) 
    texto = fuente_felicitaciones.render(mensaje, True, BLANCO) 
    rect_texto = texto.get_rect(center=(pantalla.get_width() / 2, pantalla.get_height() / 2))
    pantalla.blit(texto, rect_texto)
    pygame.display.flip()
    pygame.time.wait(4000)

def mostrar_derrota(pantalla, puntaje):
    pantalla.fill(NEGRO) 
    mensaje = f"¡Perdiste! Tu puntaje es: {puntaje}" 
    fuente_felicitaciones = pygame.font.Font(None, 50) 
    texto = fuente_felicitaciones.render(mensaje, True, BLANCO) 
    rect_texto = texto.get_rect(center=(pantalla.get_width() / 2, pantalla.get_height() / 2))
    pantalla.blit(texto, rect_texto)
    pygame.display.flip()
    pygame.time.wait(5000)