map_tab = [
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
import pygame as pg
from units import Unit

class Map:
    def __init__(self, game):
        self.game = game
        self.map_tab = map_tab
        self.map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.map_tab):
            for i, value in enumerate(row):
                self.map[(j, i)] = value

    def check_collision(self, tile):
        if self.map[tile] == 1 and self.game.unit_map.unit_map[tile[0]][tile[1]] == 1:
            return False
        return True

    def draw(self):
        for pos in self.map:
            if self.map[pos] == 1:
                pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 80, pos[1] * 80, 80, 80), 1)
            else:
                pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 80, pos[1] * 80, 80, 80), 0)

class UnitMap:
    def __init__(self, game, map_game):
        self.game = game
        self.unit_map = map_tab
        self.map = map_game

    def place_unit(self, unit, tile):
        if not self.map.check_collision(tile):
            if self.unit_map[tile[0]][tile[1]] == 1:
                self.unit_map[unit.x][unit.y] = 1
                self.unit_map[tile[0]][tile[1]] = unit
                unit.x = tile[0]
                unit.y = tile[1]

    def remove_unit(self, unit):
        if isinstance(self.unit_map[unit.x][unit.y], Unit):
            self.unit_map[unit.x][unit.y] = 1

    def draw(self):
        for x in self.unit_map:
            for y in x:
                if isinstance(y, Unit):
                    if y == self.game.unit_handler.units[self.game.turn]:
                        y.draw(gamma=255)
                    else:
                        y.draw(gamma=155)

        if self.game.hovered_tile:
            if isinstance(self.unit_map[self.game.hovered_tile[0]][self.game.hovered_tile[1]], Unit):
                unit = self.unit_map[self.game.hovered_tile[0]][self.game.hovered_tile[1]]
                font = pg.font.Font(None, 36)
                text_surface = font.render(
                    f"{unit.name}: HP={unit.hp}", True, "white")
                self.game.screen.blit(text_surface, (10, 10))
