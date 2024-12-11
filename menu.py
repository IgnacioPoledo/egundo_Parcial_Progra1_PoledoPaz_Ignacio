import pygame
from funciones import *  
from constantes import *

pygame.init()

def menu_principal(pantalla, fuente):
    imagen_nombre = pygame.image.load("Juego/imagenes/this or that.png")
    imagen_nombre = pygame.transform.scale(imagen_nombre,(900,600))

    jugando = True

    while jugando:
        pantalla.blit(imagen_nombre, (0, 0))

        botones = {
            "Jugar": pygame.Rect(350, 200, 200, 50),
            "Opciones": pygame.Rect(350, 270, 200, 50),
            "Salir": pygame.Rect(350, 340, 200, 50),
        }

        for texto, rect in botones.items():
            pygame.draw.rect(pantalla, GRIS, rect)
            mostrar_texto(pantalla, texto, rect.centerx, rect.centery, fuente, NEGRO, centrado=True)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botones["Jugar"].collidepoint(evento.pos):
                    return "jugar"
                elif botones["Opciones"].collidepoint(evento.pos):
                    return "opciones"
                elif botones["Salir"].collidepoint(evento.pos):
                    pygame.quit()
                    return "salir"
    pygame.quit()