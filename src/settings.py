import os

# 게임 화면 크기
WIDTH, HEIGHT = 1200, 700

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 0, 0) # RED

# 셀 크기
CELL_SIZE = 40

# 아이템 배열 크기
COLUMNS = 17
ROWS = 10

# 게임판의 전체 크기 (가로, 세로)
BOARD_WIDTH = COLUMNS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE

# 타이머 초기 시간
TIMER_INITIAL = 30

# 파일 경로 설정
ICON_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png"))
ITEM_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "item.png"))
CORRECT_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "chill-01.png"))
INCORRECT_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "chill-02.png"))