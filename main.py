import pygame as pg
import sys
from settings import *
from map import *
from units import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.turn = 0
        self.clicked_tile = None  # Zmienna przechowująca pole kliknięcia

    def new_game(self):
        self.map = Map(self)
        self.unit_map = UnitMap(self, self.map)
        self.unit_handler = UnitHandler(self)

    def is_within_map_bounds(self, tile):
        max_x, max_y = len(self.map.map_tab[0]), len(self.map.map_tab)
        return 0 <= tile[0] < max_x and 0 <= tile[1] < max_y

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

        if self.clicked_tile is not None:
            if self.unit_handler.take_turn(self.clicked_tile, self.turn):  # Ruch udany
                self.turn += 1
                if self.turn >= len(self.unit_handler.units):  # Reset tury
                    self.turn = 0
            self.clicked_tile = None  # Wyczyszczenie kliknięcia po obsłużeniu

    def draw(self):
        self.screen.fill("black")
        self.map.draw()
        self.unit_map.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                tile = (mouse_pos[0] // 80, mouse_pos[1] // 80)  # Zamiana na współrzędne siatki
                if self.is_within_map_bounds(tile):  # Sprawdzenie granic mapy
                    self.clicked_tile = tile

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    K0 = Knight(0, 0, "red", game)
    K1 = Knight(9, 9, "blue", game)
    K2 = Knight(0, 9, "red", game)
    K3 = Knight(9, 0, "blue", game)
    game.unit_map.place_unit(K0, (0, 0))
    game.unit_map.place_unit(K1, (9, 9))
    game.unit_map.place_unit(K2, (0, 9))
    game.unit_map.place_unit(K3, (9, 0))
    game.unit_handler.add_unit(K0)
    game.unit_handler.add_unit(K1)
    game.unit_handler.add_unit(K2)
    game.unit_handler.add_unit(K3)
    game.run()
