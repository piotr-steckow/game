import pygame as pg
import sys
from settings import *
from map import *
from units import *
from random import randint

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.turn = 0
    def new_game(self):
        self.map = Map(self)
        self.unit_map = UnitMap(self, self.map)
        self.unit_handler = UnitHandler(self)

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        x = randint(0,9)
        y = randint(0,9)
        print(x,y)
        self.unit_handler.take_turn((x,y), self.turn)
        self.turn += 1
        if self.turn == 4:
            self.turn = 0

    def draw(self):
        self.screen.fill("black")
        self.map.draw()
        self.unit_map.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    x = 0
    y = 0
    K0 = Knight(0, 0, game)
    K1 = Knight(9, 9, game)
    K2 = Knight(0, 9, game)
    K3 = Knight(9, 0, game)
    game.unit_map.place_unit(K0, (0, 0))
    game.unit_map.place_unit(K1, (9, 9))
    game.unit_map.place_unit(K2, (0, 9))
    game.unit_map.place_unit(K3, (9, 0))
    game.unit_handler.add_unit(K0)
    game.unit_handler.add_unit(K1)
    game.unit_handler.add_unit(K2)
    game.unit_handler.add_unit(K3)
    game.run()