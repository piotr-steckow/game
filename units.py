import pygame as pg

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
        if not self.dead:
            current_pos = (self.x, self.y)
            target_pos = tile
            distance = abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])

            if distance > self.speed:
                return False

            if not self.game.map.check_collision(target_pos):
                self.game.unit_map.place_unit(self, target_pos)
                self.take_damage(20)
                return True

            return False


    def draw(self, gamma=255):
        if not self.dead:
            if self.team == "red":
                color = (gamma,0,0)
            elif gamma != 255:
                color = (25,25,gamma)
            else:
                color = (100,100,gamma)
            pg.draw.circle(self.game.screen, color, (self.x*80 + 40, self.y*80 + 40), 25)

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
        super().__init__(x, y, game, name="Crossbowman", hp=60, atk=40, range=4, speed=1, cost=75)
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
        return unit.move(tile)

    def display_current_unit(self):
        font = pg.font.Font(None, 36)
        current_unit = self.units[self.game.turn]
        text_surface = font.render(f"Turn: {current_unit.name}, Player: {current_unit.team}", True, "white")
        text_rect = text_surface.get_rect(topright=(self.game.screen.get_width() - 10, 10))
        self.game.screen.blit(text_surface, text_rect)

    def remove_dead_units(self):
        dead_units = [unit for unit in self.units if unit.dead]
        for unit in dead_units:
            self.game.unit_map.remove_unit(unit)
            self.units.remove(unit)
            del unit

        new_dead = False
        if dead_units:
            new_dead = True

        return len(dead_units), new_dead

