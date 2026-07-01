"""
splash.py
~~~~~~~~~
Pygame opening logo with mild background music.
"""
import os
import time
import pygame as p

from .config import LOGO_FILE, MUSIC_FILE


def show_splash(seconds: int = 6, size=(820, 620)):
    """Display the BrainBolt logo + play the opening tune."""
    if not os.path.exists(LOGO_FILE):
        print("(logo file not found - skipping splash)")
        return

    p.init()
    p.display.init()
    p.display.set_caption("BrainBolt - Spark Your Mind")
    screen = p.display.set_mode(size)

    raw = p.image.load(LOGO_FILE)
    try:
        raw = raw.convert()
    except p.error:
        raw = raw.convert_alpha()
    img = p.transform.smoothscale(raw, size)

    music_loaded = False
    if os.path.exists(MUSIC_FILE):
        try:
            p.mixer.init()
            p.mixer.music.load(MUSIC_FILE)
            p.mixer.music.set_volume(0.5)
            p.mixer.music.play()
            music_loaded = True
        except Exception as e:
            print("(music could not play:", e, ")")

    clock = p.time.Clock()
    end = time.time() + seconds
    while time.time() < end:
        for ev in p.event.get():
            if ev.type == p.QUIT:
                end = 0
        screen.fill((10, 12, 30))
        screen.blit(img, (0, 0))
        p.display.flip()
        clock.tick(30)

    if music_loaded:
        try:
            p.mixer.music.fadeout(800)
            time.sleep(0.8)
        except Exception:
            pass
    p.quit()
