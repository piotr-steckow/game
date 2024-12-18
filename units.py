import pygame as pg
from map import Map

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

    def take_damage(self, damage):
        self.hp -= damage
        if self.check_death():
            self.dead = True

    def check_death(self):
        if self.hp <= 0:
            return True
        else:
            return False

    def move(self, tile):
        if not self.game.map.check_collision(tile):
            self.game.unit_map.place_unit(self, tile)

    def draw(self):
        pg.draw.circle(self.game.screen, "white", (self.x*80 + 40, self.y*80 + 40), 25)

class Knight(Unit):
    def __init__(self, x, y, game):
        super().__init__(x, y, game, name="Knight", hp=150, atk=40, range=1, speed=3, cost=150)
        self.dead = False
        self.x = x
        self.y = y
        self.game = game

class Archer(Unit):
    def __init__(self, x, y):
        super().__init(x, y, name="Archer", hp=40, atk=30, range=5, speed=2, cost=50)


class Crossbowman(Unit):
    def __init__(self, x, y):
        super().__init(x, y, name="Crossbowman", hp=60, atk=40, range=4, speed=1, cost=75)


class Footman(Unit):
    def __init__(self, x, y):
        super().__init(x, y, name="Footman", hp=80, atk=20, range=1, speed=2, cost=25)


class DeathKnight(Unit):
    def __init__(self, x, y):
        super().__init(x, y, name="Footman", hp=140, atk=20, range=1, speed=2, cost=200)
        self.lifesteal = 10

class UnitHandler:
    def __init__(self, game):
        self.units = []
        self.game = game

    def add_unit(self, unit):
        self.units.append(unit)

    def take_turn(self, tile, turn_id):
        unit = self.units[turn_id]
        unit.move(tile)
