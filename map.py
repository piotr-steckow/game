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


    def draw(self):
        for x in self.unit_map:
            for y in x:
                if y != 1 and y != 0:
                    y.draw()

