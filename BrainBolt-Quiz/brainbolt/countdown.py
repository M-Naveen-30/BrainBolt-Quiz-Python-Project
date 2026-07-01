"""
countdown.py
~~~~~~~~~~~~
Big 3-2-1 countdown in a Pygame window before the quiz starts.
"""
import time
import pygame as p


def countdown(size=(640, 480)):
    p.init()
    p.display.init()
    p.display.set_caption("Get Ready - BrainBolt")
    screen = p.display.set_mode(size)
    font   = p.font.SysFont(None, 360, bold=True)
    sub    = p.font.SysFont(None, 48,  bold=True)

    clock = p.time.Clock()
    for n, colour in [(3, (255, 80, 80)),
                      (2, (255, 200, 60)),
                      (1, (80, 220, 120))]:
        end = time.time() + 1.0
        while time.time() < end:
            for ev in p.event.get():
                if ev.type == p.QUIT:
                    end = 0
            screen.fill((12, 14, 32))
            big = font.render(str(n), True, colour)
            sm  = sub.render("Get Ready!", True, (220, 220, 230))
            screen.blit(big,  big.get_rect(center=(size[0] // 2, size[1] // 2)))
            screen.blit(sm,   sm.get_rect(center=(size[0] // 2, 70)))
            p.display.flip()
            clock.tick(30)

    # final GO!
    end = time.time() + 0.7
    while time.time() < end:
        for ev in p.event.get():
            if ev.type == p.QUIT:
                end = 0
        screen.fill((10, 30, 18))
        big = font.render("GO!", True, (140, 255, 160))
        screen.blit(big, big.get_rect(center=(size[0] // 2, size[1] // 2)))
        p.display.flip()
        clock.tick(30)

    p.quit()
