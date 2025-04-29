import pygame
import random
from settings import *

class Item:
    def __init__(self, x, y, offset_x, offset_y):
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.number = random.randint(1, 6)
        self.rect = pygame.Rect(
            self.offset_x + self.x * CELL_SIZE,
            self.offset_y + self.y * CELL_SIZE,
            CELL_SIZE, CELL_SIZE
        )

        # 아이템 이미지 로딩
        self.image = pygame.image.load(ITEM_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def draw(self, screen, highlight=False):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # 숫자 폰트
        font = pygame.font.SysFont("Arial", 24)
        number_text = font.render(str(self.number), True, BLACK)

        # 숫자 정렬
        text_width = number_text.get_width()
        text_height = number_text.get_height()
        text_x = self.x * CELL_SIZE + self.offset_x + (CELL_SIZE - text_width) // 2
        text_y = self.y * CELL_SIZE + self.offset_y + (CELL_SIZE - text_height) // 2

        screen.blit(number_text, (text_x, text_y))

        if highlight:
            self.highlight_item(screen)

    def highlight_item(self, screen):
        highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        highlight_surface.fill((255, 0, 0, 200)) # RED HIGHLIGHT
        screen.blit(highlight_surface, self.rect.topleft, special_flags = pygame.BLEND_RGBA_ADD)