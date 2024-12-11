import pygame
from constantes import *
from funciones import *

pygame.init()

volumen = 100
musica_muted = False

fuente_boton = pygame.font.SysFont("Arial Rounded MT Bold", 23)
fuente_volumen = pygame.font.SysFont("Arial Rounded MT Bold", 50)
fuente_cartel_volumen = pygame.font.SysFont("Arial Rounded MT Bold", 40)  # TÍTULO

boton_suma = {"superficie": pygame.Surface(TAMAÑO_BOTON_SUMA), "rectangulo": pygame.Rect(0, 0, 0, 0)}
boton_suma['superficie'].fill(AZUL)

boton_resta = {"superficie": pygame.Surface(TAMAÑO_BOTON_SUMA), "rectangulo": pygame.Rect(0, 0, 0, 0)}
boton_resta['superficie'].fill(AZUL)

boton_volver = {"superficie": pygame.Surface(TAMAÑO_BOTON_VOLVER), "rectangulo": pygame.Rect(0, 0, 0, 0)}
boton_volver['superficie'].fill(ROJO)

volumen_encendido = pygame.image.load("Juego/imagenes/activo.png")
volumen_encendido = pygame.transform.scale(volumen_encendido, (90, 90))
rect_vol_on = volumen_encendido.get_rect()
rect_vol_on.centerx = 280
rect_vol_on.centery = 360

volumen_apagado = pygame.image.load("Juego/imagenes/mute.png")
volumen_apagado = pygame.transform.scale(volumen_apagado, (90, 90))
rect_vol_off = volumen_apagado.get_rect()
rect_vol_off.centerx = 580
rect_vol_off.centery = 360

click_sonido = pygame.mixer.Sound("Juego/sonidos/sonidos_click.mp3")
click_sonido.set_volume(1)

def sincronizar_sonidos():
    if musica_muted:
        click_sonido.set_volume(0)
        pygame.mixer.music.set_volume(0)
    else:
        click_sonido.set_volume(volumen / 100)
        pygame.mixer.music.set_volume(volumen / 100)

def mostrar_opciones(pantalla: pygame.Surface, eventos):
    global volumen, musica_muted
    retorno = "opciones"

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_suma["rectangulo"].collidepoint(evento.pos):
                if volumen < 96 and not musica_muted:
                    volumen += 5
                    sincronizar_sonidos()
                    click_sonido.play()
            elif boton_resta["rectangulo"].collidepoint(evento.pos):
                if volumen > 0 and not musica_muted:
                    volumen -= 5
                    sincronizar_sonidos()
                    click_sonido.play()
            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                retorno = "menu"
                click_sonido.play()
            elif rect_vol_off.collidepoint(evento.pos):
                musica_muted = True
                sincronizar_sonidos()
            elif rect_vol_on.collidepoint(evento.pos):
                musica_muted = False
                sincronizar_sonidos()
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    pantalla.fill(NEGRO)

    titulo_boton = fuente_cartel_volumen.render("AJUSTAR SONIDO", True, AZUL)
    pantalla.blit(titulo_boton, (300, 100))
    boton_resta["rectangulo"] = pantalla.blit(boton_resta["superficie"], (150, 200))
    boton_suma["rectangulo"] = pantalla.blit(boton_suma["superficie"], (650, 200))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver["superficie"], (5, 5))

    pantalla.blit(volumen_encendido, rect_vol_on)
    pantalla.blit(volumen_apagado, rect_vol_off)

    blit_text(boton_suma["superficie"], " VOL+", (10, 10), fuente_boton, BLANCO)
    blit_text(boton_resta["superficie"], "VOL -", (10, 10), fuente_boton, BLANCO)
    blit_text(pantalla, f"{volumen} %", (380, 200), fuente_volumen, GRIS)
    blit_text(boton_volver["superficie"], "VOLVER", (10, 10), fuente_boton, BLANCO)

    return retorno
