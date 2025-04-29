import random
import pygame
from game_item import Item
from game_timer import Timer
from settings import *

class Game:
    def __init__(self):
        pygame.init()

        # 화면 설정
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Are you chill?")

        # 아이콘 설정
        icon_image = pygame.image.load(ICON_IMAGE_PATH)
        pygame.display.set_icon(icon_image)

        # 게임판의 중앙 배치를 위한 오프셋 계산
        self.offset_x = (WIDTH - BOARD_WIDTH) // 2
        self.offset_y = (HEIGHT - BOARD_HEIGHT) // 2

        # 아이템 객체 생성
        self.items = [Item(x, y, self.offset_x, self.offset_y) for x in range(COLUMNS) for y in range(ROWS)]

        # 타이머 객체 생성
        self.timer = Timer()

        # 점수
        self.score = 0

        # 게임 오버 상태
        self.game_over_flag = False

        # 아이템 이미지 로드
        self.correct_image = pygame.image.load(CORRECT_IMAGE_PATH)
        self.incorrect_image = pygame.image.load(INCORRECT_IMAGE_PATH)

        # 드래그 관련 변수
        self.dragging = False
        self.drag_start = None
        self.drag_rect = None

        # 특별 이벤트 실행 여부 플래그
        self.freeze_effect_triggered = False

    def draw_score(self):
        font = pygame.font.SysFont("Arial", 22)
        score_text = font.render(f"chill stack: {self.score}", True, BLACK)
        self.screen.blit(score_text, (200, 100))

    def draw_timer_bar(self):
        self.timer.draw(self.screen, WIDTH)

    def update(self):
        self.timer.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # 종료
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 드래그 시작
                if event.button == 1: # 왼쪽 마우스 버튼 클릭
                    self.dragging = True
                    self.drag_start = event.pos
                    self.drag_rect = pygame.Rect(self.drag_start[0], self.drag_start[1], 0, 0) # 드래그 범위 초기화
            elif event.type == pygame.MOUSEBUTTONUP:
                # 드래그 종료
               if event.button == 1:
                    self.dragging = False
                    selected_items = []
                    total_sum = 0

                    # 드래그 범위 내에 포함된 아이템의 합 계산
                    for item in self.items:
                        if self.drag_rect.colliderect(item.rect):
                            selected_items.append(item)
                            total_sum += item.number

                    # 합이 7인 경우 아이템 제거
                    if total_sum == 7:
                        removed_count = len(selected_items) # 삭제된 아이템 개수
                        for item in selected_items:
                            self.items.remove(item)
                        self.score += removed_count
                        self.show_image_with_fade(self.correct_image, position=(50, HEIGHT - self.correct_image.get_height() - 20), duration = 1.2)
                    else:
                       # 틀린 경우에는 틀린 이미지 표시
                        self.show_image_with_fade(self.incorrect_image, position=(50, HEIGHT - self.incorrect_image.get_height() - 20), duration = 1.2)

                    self.drag_rect = None # 드래그 영역 초기화
            elif event.type == pygame.MOUSEMOTION:
                # 마우스 이동 시 드래그 영역 업데이트
                if self.dragging:
                    # 드래그된 범위 갱신
                    new_width = event.pos[0] - self.drag_start[0]
                    new_height = event.pos[1] - self.drag_start[1]

                    # 드래그 범위가 마이너스가 되지 않도록 조정
                    self.drag_rect.width = new_width if new_width > 0 else -new_width # width가 음수일 경우 반대로 설정
                    self.drag_rect.height = new_height if new_height > 0 else -new_height # height가 음수일 경우 반대로 설정

                    # 드래그 범위의 위치를 시작점으로 맞추기 위해 시작점 위치를 업데이트
                    self.drag_rect.left = self.drag_start[0] if new_width >= 0 else event.pos[0]
                    self.drag_rect.top = self.drag_start[1] if new_height >= 0 else event.pos[1]

                    # 드래그 범위가 화면을 벗어나지 않도록 제한
                    if self.drag_rect.left < 0:
                        self.drag_rect.left = 0
                    if self.drag_rect.top < 0:
                        self.drag_rect.top = 0
                    if self.drag_rect.right > WIDTH:
                        self.drag_rect.right = WIDTH
                    if self.drag_rect.bottom > HEIGHT:
                        self.drag_rect.bottom = HEIGHT

        return True # 게임 실행 유지지

    def show_image_with_fade(self, image, position, duration=1):
        fade_surface = image.convert_alpha() # 알파 채널을 지원하는 Surface로 변환
        alpha = 255 # 처음에는 완전 불투명

        # 이미지가 사라질 시간 동안 서서히 알파값을 줄임
        start_time = pygame.time.get_ticks() # 시작 시간

        while pygame.time.get_ticks() - start_time < duration * 1000: # duration초 동안
            # 알파 값 줄이기
            elapsed_time = pygame.time.get_ticks() - start_time
            alpha = max(0, 255 - (elapsed_time / (duration * 1000)) * 255) # 알파값을 서서히 줄여줌
            fade_surface.set_alpha(alpha) # 새로운 알파 값 설정

            self.screen.fill((230, 230, 230)) # 배경 채우기
            for item in self.items:
                item.draw(self.screen)

            self.draw_score()
            self.draw_timer_bar()
            self.screen.blit(fade_surface, position)
            pygame.display.update()

            pygame.time.delay(10)

    def freeze_effect(self):
        # 화면 프리즈
        ice_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ice_surface.fill((0, 255, 255, 50)) # 반투명으로 채우기

        # 애니메이션
        for i in range(0, 200, 5):
            ice_surface.set_alpha(i) # 알파값을 증가시켜 투명도 증가
            self.screen.blit(ice_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(50) # 효과 간격

    def freeze_items(self):
        # 아이템을 랜덤하게 섞어 순서 변경
        random.shuffle(self.items)

        for item in self.items:
            # 아이템 프리즈
            ice_layer = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            ice_layer.fill((0, 255, 255, 100)) # 투명한 얼음 레이어

            # 애니메이션
            for i in range(0, 255, 10):
                ice_layer.set_alpha(i) # 알파값을 증가시켜 투명도 증가
                self.screen.blit(item.image, (item.rect.x, item.rect.y))
                self.screen.blit(ice_layer, (item.rect.x, item.rect.y))
                pygame.display.update()
                pygame.time.delay(5) # 효과 간격

    def game_freeze_effect(self):
        # 게임 프리즈
        font = pygame.font.SysFont("Arial", 50)
        freeze_message = font.render("TOO CHILL!!", True, WHITE)

        start_time = pygame.time.get_ticks()
        duration = 2000

        while pygame.time.get_ticks() - start_time < duration:
            # 메시지 그리기
            self.screen.blit(freeze_message, (WIDTH // 2 - freeze_message.get_width() // 2, HEIGHT // 2 - freeze_message.get_height() // 2))
            pygame.display.update()

            # 잠시 대기 (60FPS로 제한)
            pygame.time.Clock().tick(60)

        # 메시지 표시 후 원래 화면으로 돌아가게 처리
        self.screen.fill((230, 230, 230))
        self.draw_score()
        self.draw_timer_bar()
        pygame.display.update()

    def run(self):
        running = True
        while running:
            self.screen.fill((230, 230, 230)) # 배경 색

            self.update() # 타이머 업데이트

            if not self.game_over_flag:
                # 이벤트 처리
                running = self.handle_events()

                # 아이템 그리기
                for item in self.items:
                    highlight = False
                    if self.drag_rect and self.drag_rect.colliderect(item.rect):
                        highlight = True
                    item.draw(self.screen, highlight) # 하이라이트 인자로 추가

                # 점수 그리기
                self.draw_score()

                # 타이머 표시
                self.draw_timer_bar()

                # 점수 77달성 시 특별 이벤트
                if self.score == 77 and not self.freeze_effect_triggered:
                    self.freeze_effect() # 게임판 얼음 효과
                    self.freeze_items() # 아이템 얼음 효과
                    self.game_freeze_effect() # 게임 일시 프리즈

                    # 이벤트가 한번만 실행되도록 플래그 설정
                    self.freeze_effect_triggered = True

            pygame.display.update()

        pygame.quit()