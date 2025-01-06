from operator import index

import pygame as pg
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Unit:
    def __init__(self, x, y, game, name, hp, atk, range, speed, cost):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.atk = atk
        self.range = range
        self.speed = speed
        self.cost = cost
        self.dead = False
        self.game = game
        self.grid = Grid(matrix=self.game.unit_map.unit_map)
        self.finder = AStarFinder()
        self.ready_to_attack = False

    def take_damage(self, damage):
        self.hp -= damage
        if self.check_death():
            self.dead = True

    def check_death(self):
        return self.hp <= 0

    def attack(self, tile):
        if not self.dead:
            target_unit = self.game.unit_map.unit_map[tile[0]][tile[1]]
            if (
                    self.calculate_attack_distance(tile) <= self.range
                    and isinstance(target_unit, Unit)
                    and target_unit != self
                    and target_unit.team != self.team
            ):
                target_unit.take_damage(self.atk)
                if target_unit.dead and self.name == "Knight" or self.name == "Footman":
                    self.game.unit_map.place_unit(self, tile)
                return True
            elif self.name == "Knight" or self.name == "Footman":
                if tile == (self.x - 1, self.y -1) or tile == (self.x + 1, self.y -1) or tile == (self.x - 1, self.y +1) or tile == (self.x + 1, self.y +1):
                    if isinstance(target_unit, Unit) and target_unit.team != self.team:
                        target_unit.take_damage(self.atk)
                        return True
        return False

    def move(self, tile):
        if self.dead:
            return False

        target_pos = tile
        distance = self.calculate_distance_to(target_pos)

        if distance > self.speed:
            return False

        if not self.game.map.check_collision(target_pos):
            self.game.unit_map.place_unit(self, target_pos)
            return True

        return False

    def can_attack(self):
        can_attack = False
        for x in range(len(self.game.map.map_tab[0])):
            for y in range(len(self.game.map.map_tab)):
                if self.calculate_attack_distance((x, y)) <= self.range and isinstance(
                        self.game.unit_map.unit_map[x][y], Unit) and self.game.unit_map.unit_map[x][
                    y].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (x * 80, y * 80, 80, 80), 3)
                    can_attack = True
        if self.name == "Knight" or self.name =="Footman":
            if self.x!= 9 and self.y!= 9:
                if isinstance(self.game.unit_map.unit_map[self.x+1][self.y+1], Unit) and self.game.unit_map.unit_map[self.x+1][self.y+1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80 + 80, self.y * 80+80, 80, 80), 3)
                    can_attack = True
            if self.x!= 0 and self.y != 9:
                if isinstance(self.game.unit_map.unit_map[self.x-1][self.y+1], Unit) and self.game.unit_map.unit_map[self.x-1][self.y+1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80-80, self.y * 80+80, 80, 80), 3)
                    can_attack = True
            if self.x!= 0 and self.y != 0:
                if isinstance(self.game.unit_map.unit_map[self.x-1][self.y-1], Unit) and self.game.unit_map.unit_map[self.x-1][self.y-1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80-80, self.y * 80-80, 80, 80), 3)
                    can_attack = True
            if self.x!=9 and self.y !=0:
                if isinstance(self.game.unit_map.unit_map[self.x+1][self.y-1], Unit) and self.game.unit_map.unit_map[self.x+1][self.y-1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80+80, self.y * 80-80, 80, 80), 3)
                    can_attack = True
        return can_attack

    def calculate_distance_to(self, target_pos):
        processed_map = self.get_processed_map()
        self.grid = Grid(matrix=processed_map)
        start = self.grid.node(self.y, self.x)
        end = self.grid.node(target_pos[1], target_pos[0])
        path, runs = self.finder.find_path(start, end, self.grid)
        if path:
            return len(self.finder.find_path(start, end, self.grid)[0]) - 1
        else:
            return 100

    def calculate_attack_distance(self, target_pos):
        processed_map = self.get_processed_attack_map()
        self.grid = Grid(matrix=processed_map)
        start = self.grid.node(self.y, self.x)
        end = self.grid.node(target_pos[1], target_pos[0])
        return len(self.finder.find_path(start, end, self.grid)[0]) - 1

    def get_processed_map(self):
        return [[1 if cell == 1 else 0 for cell in row] for row in self.game.unit_map.unit_map]

    def get_processed_attack_map(self):
        return [[1 if cell == 0 else 1 for cell in row] for row in self.game.unit_map.unit_map]

    def draw(self, gamma=255):
        if self.dead:
            return

        color = self.get_unit_color(gamma)
        pg.draw.circle(self.game.screen, color, (self.x * 80 + 40, self.y * 80 + 40), 25)

        if self.game.unit_handler.units[self.game.turn] == self:
            if self.ready_to_attack:
                self.highlight_valid_attacks()
            else:
                self.highlight_valid_moves(gamma)
                self.highlight_valid_attacks()

    def get_unit_color(self, gamma):
        if self.team == "red":
            return (gamma, 0, 0)
        elif gamma != 255:
            return (25, 25, gamma)
        return (100, 100, gamma)

    def highlight_valid_moves(self, gamma):
        for x in range(len(self.game.map.map_tab[0])):
            for y in range(len(self.game.map.map_tab[0])):
                if self.calculate_distance_to((x, y)) <= self.speed and not self.game.map.check_collision((x, y)):
                    pg.draw.rect(self.game.screen, "white", (x * 80, y * 80, 80, 80), 3)

    def highlight_valid_attacks(self):
        for x in range(len(self.game.map.map_tab[0])):
            for y in range(len(self.game.map.map_tab)):
                if self.calculate_attack_distance((x, y)) <= self.range and isinstance(
                        self.game.unit_map.unit_map[x][y], Unit) and self.game.unit_map.unit_map[x][
                    y].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (x * 80, y * 80, 80, 80), 3)
        if self.name == "Knight" or self.name == "Footman":
            if self.x != 9 and self.y != 9:
                if isinstance(self.game.unit_map.unit_map[self.x + 1][self.y + 1], Unit) and self.game.unit_map.unit_map[self.x + 1][self.y + 1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80 + 80, self.y * 80 + 80, 80, 80), 3)
            if self.x != 0 and self.y != 9:
                if isinstance(self.game.unit_map.unit_map[self.x - 1][self.y + 1], Unit) and self.game.unit_map.unit_map[self.x - 1][self.y + 1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80 - 80, self.y * 80 + 80, 80, 80), 3)
            if self.x != 0 and self.y != 0:
                if isinstance(self.game.unit_map.unit_map[self.x - 1][self.y - 1], Unit) and self.game.unit_map.unit_map[self.x - 1][self.y - 1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80 - 80, self.y * 80 - 80, 80, 80), 3)
            if self.x != 9 and self.y != 0:
                if isinstance(self.game.unit_map.unit_map[self.x + 1][self.y - 1], Unit) and self.game.unit_map.unit_map[self.x + 1][self.y - 1].team != self.team:
                    pg.draw.rect(self.game.screen, "red", (self.x * 80 + 80, self.y * 80 - 80, 80, 80), 3)


class Knight(Unit):
    def __init__(self, x, y, team, game):
        super().__init__(x, y, game, name="Knight", hp=150, atk=40, range=1, speed=3, cost=150)
        self.team = team


class Archer(Unit):
    def __init__(self, x, y, team, game):
        super().__init__(x, y, game, name="Archer", hp=40, atk=30, range=5, speed=2, cost=50)
        self.team = team


class Crossbowman(Unit):
    def __init__(self, x, y, team, game):
        super().__init__(x, y, game, name="Crossbowman", hp=60, atk=40, range=4, speed=2, cost=75)
        self.team = team


class Footman(Unit):
    def __init__(self, x, y, team, game):
        super().__init__(x, y, game, name="Footman", hp=80, atk=20, range=1, speed=2, cost=25)
        self.team = team


class DeathKnight(Unit):
    def __init__(self, x, y, team, game):
        super().__init__(x, y, game, name="Footman", hp=140, atk=20, range=1, speed=2, cost=200)
        self.lifesteal = 10
        self.team = team


class UnitHandler:
    def __init__(self, game):
        self.units = []
        self.game = game

    def add_unit(self, unit):
        self.units.append(unit)

    def take_turn(self, tile, turn_id):
        unit = self.units[turn_id]

        if not unit.ready_to_attack:
            if (
                    unit.calculate_attack_distance(tile) <= unit.range
                    and isinstance(self.game.unit_map.unit_map[tile[0]][tile[1]], Unit)
                    and self.game.unit_map.unit_map[tile[0]][tile[1]].team != unit.team
            ):
                if unit.attack(tile):
                    return True
            elif unit.name == "Knight" or unit.name == "Footman":
                if tile == (unit.x - 1, unit.y -1) or tile == (unit.x + 1, unit.y -1) or tile == (unit.x - 1, unit.y +1) or tile == (unit.x + 1, unit.y +1):
                    if isinstance(self.game.unit_map.unit_map[tile[0]][tile[1]], Unit) and self.game.unit_map.unit_map[tile[0]][tile[1]].team != unit.team:
                        if unit.attack(tile):
                            return True

            if unit.move(tile):
                unit.ready_to_attack = unit.can_attack()
                return not unit.ready_to_attack

        elif unit.ready_to_attack:
            if unit.attack(tile):
                unit.ready_to_attack = False
                return True

        return False

    def display_current_unit(self):
        font = pg.font.Font(None, 72)
        current_unit = self.units[self.game.turn]
        text_surface = font.render(f"Turn: {current_unit.name}, Player: {current_unit.team}", True, "white")
        text_rect = text_surface.get_rect(topright=(self.game.screen.get_width() - 10, 10))
        self.game.screen.blit(text_surface, text_rect)

    def remove_dead_units(self):
        dead_index = 100
        dead_units = [unit for unit in self.units if unit.dead]
        for unit in dead_units:
            dead_index = self.units.index(unit)
            self.remove_unit(unit)
        return len(dead_units), bool(dead_units), dead_index

    def remove_unit(self, unit):
        self.game.unit_map.remove_unit(unit)
        self.units.remove(unit)
        del unit
