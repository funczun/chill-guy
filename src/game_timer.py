import pygame
from settings import HEIGHT, TIMER_INITIAL

class Timer:
    def __init__(self):
        self.time_remaining = TIMER_INITIAL
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_update_time

        if elapsed_time >= 100:
            self.last_update_time = current_time
            if self.time_remaining > 0:
                self.time_remaining -= 0.1
            if self.time_remaining <= 0:
                self.time_remaining = 0

    def draw(self, screen, width):
        # 타이머 막대 그리기
        pygame.draw.rect(screen, (200, 200, 200), (width - 200, (HEIGHT - 400) // 2, 20, 400))
        bar_height = (self.time_remaining / TIMER_INITIAL) * 400
        pygame.draw.rect(screen, (0, 255, 0), (width - 200, (HEIGHT - 400) // 2 + (400 - bar_height), 20, bar_height))