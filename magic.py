import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            sound = pygame.mixer.Sound(MAGIC_DATA['heal']['sound'])
            sound.set_volume(0.1)
            sound.play()
            player.health += strength
            player.energy -= cost

            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            offset = pygame.math.Vector2(0, -60)
            self.animation_player.create_particles('heal', player.rect.center + offset, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            sound = pygame.mixer.Sound(MAGIC_DATA['flame']['sound'])
            sound.set_volume(0.1)
            sound.play()
            player.energy -= cost

            direction = player.status.split('_')[0]
            if direction == 'right': direction_vec = pygame.math.Vector2(1, 0)
            elif direction == 'left': direction_vec = pygame.math.Vector2(-1, 0)
            elif direction == 'down': direction_vec = pygame.math.Vector2(0, 1)
            else: direction_vec = pygame.math.Vector2(0, -1)

            for i in range(1, 6):
                if direction_vec.x:  # horizontal flames
                    offset_x = direction_vec.x * i * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # vertical flames
                    offset_y = direction_vec.y * i * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
