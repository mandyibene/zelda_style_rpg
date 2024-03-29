import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dict
        self.weapon_graphics = self.import_graphics(WEAPON_DATA)

        # convert magic dict
        self.magic_graphics = self.import_graphics(MAGIC_DATA)

    def import_graphics(self, dictionary):
        graphics = []
        for item in dictionary.values():
            path = item['graphic']
            item = pygame.image.load(path).convert_alpha()
            graphics.append(item)
        return graphics

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        width = self.display_surface.get_size()[0] - 20
        height = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(width, height))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def display_overlay(self, left, top, style, index, has_switched):
        bg_rect = self.selection_box(left, top, has_switched)
        if style == 'weapon':
            surf = self.weapon_graphics[index]
        else:
            surf = self.magic_graphics[index]
        rect = surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(surf, rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.display_overlay(10, 610, 'weapon', player.weapon_index, not player.can_switch_weapon)
        self.display_overlay(80, 630, 'magic', player.magic_index, not player.can_switch_magic)
