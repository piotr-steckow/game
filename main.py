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
        self.clicked_tile = None
        self.hovered_tile = None

    def new_game(self):
        self.map = Map(self)
        self.unit_map = UnitMap(self, self.map)
        self.unit_handler = UnitHandler(self)

    def is_within_map_bounds(self, tile):
        max_x, max_y = len(self.map.map_tab[0]), len(self.map.map_tab)
        return 0 <= tile[0] < max_x and 0 <= tile[1] < max_y

    def end_game(self, condition):
        if condition != False:
            print(condition, "won")
            pg.quit()
            sys.exit()

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

        if self.clicked_tile is not None:
            if self.unit_handler.take_turn(self.clicked_tile, self.turn):
                self.turn += 1

        removed_count, new_dead, dead_index = self.unit_handler.remove_dead_units()
        if new_dead:
            if self.unit_handler.units[self.turn-1].name == "Footman" or self.unit_handler.units[self.turn-1].name == "Knight":
                self.unit_handler.units[self.turn-1].move(self.clicked_tile)
        self.clicked_tile = None

        if new_dead and dead_index < self.turn:
            self.turn -= 1
        if self.turn >= len(self.unit_handler.units):
            self.turn = 0

        end = self.unit_handler.check_victory()
        self.end_game(end)

    def draw(self):
        self.screen.fill("black")
        self.map.draw()
        self.unit_map.draw()
        self.unit_handler.display_current_unit()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                tile = (mouse_pos[0] // 80, mouse_pos[1] // 80)
                if self.is_within_map_bounds(tile):
                    self.clicked_tile = tile
            elif event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()
                tile = (mouse_pos[0] // 80, mouse_pos[1] // 80)
                if self.is_within_map_bounds(tile):
                    self.hovered_tile = tile

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()

    # Create Red Team Units
    R0 = Knight(2, 0, "red", game)
    R1 = Archer(3, 0, "red", game)
    R2 = Footman(4, 0, "red", game)
    R3 = Knight(5, 0, "red", game)
    R4 = Crossbowman(6, 0, "red", game)

    # Create Blue Team Units
    B0 = Knight(2, 9, "blue", game)
    B1 = Archer(3, 9, "blue", game)
    B2 = Footman(4, 9, "blue", game)
    B3 = Knight(5, 9, "blue", game)
    B4 = Crossbowman(6, 9, "blue", game)

    # Place Red Team Units
    game.unit_map.place_unit(R0, (2, 0))
    game.unit_map.place_unit(R1, (3, 0))
    game.unit_map.place_unit(R2, (4, 0))
    game.unit_map.place_unit(R3, (5, 0))
    game.unit_map.place_unit(R4, (6, 0))

    # Place Blue Team Units
    game.unit_map.place_unit(B0, (2, 9))
    game.unit_map.place_unit(B1, (3, 9))
    game.unit_map.place_unit(B2, (4, 9))
    game.unit_map.place_unit(B3, (5, 9))
    game.unit_map.place_unit(B4, (6, 9))

    # Add Units to UnitHandler
    game.unit_handler.add_unit(R0)
    game.unit_handler.add_unit(R1)
    game.unit_handler.add_unit(R2)
    game.unit_handler.add_unit(R3)
    game.unit_handler.add_unit(R4)
    game.unit_handler.add_unit(B0)
    game.unit_handler.add_unit(B1)
    game.unit_handler.add_unit(B2)
    game.unit_handler.add_unit(B3)
    game.unit_handler.add_unit(B4)

    game.run()


