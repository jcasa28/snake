import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
HEADER_HEIGHT = 100
FPS_OPTIONS = {'hard': 30, 'medium': 20, 'easy': 12}
DEFAULT_FPS = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

#font for the display
FONT = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), ((cur[1] + (y * GRID_SIZE)) % HEIGHT))

        # Check if snake is colliding with itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#function for displaying text
def draw_text(surface, text, position, color=WHITE):
    text_surface = FONT.render(text, True, color)
    surface.blit(text_surface, position)

def draw_button(surface, text, rect, color=GRAY):
    pygame.draw.rect(surface, color, rect)
    draw_text(surface, text, (rect[0] + 10, rect[1] + 5))
def resume_draw_button(surface, text, rect, color=GREEN):
    pygame.draw.rect(surface, color, rect)
    draw_text(surface, text, (rect[0] + 10, rect[1] + 5))

def start_screen(screen):
    button_width, button_height = 100, 50
    button_spacing = 20
    easy_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - button_spacing, button_width, button_height)
    medium_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
    hard_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_height + button_spacing, button_width, button_height)

    while True:
        screen.fill(BLACK)
        draw_text(screen, "Welcome to the Culebrita", (WIDTH // 2 - 150, HEIGHT // 2 - 150), WHITE)
        draw_button(screen, "Easy", easy_button)
        draw_button(screen, "Medium", medium_button)
        draw_button(screen, "Hard", hard_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    return FPS_OPTIONS['easy']
                elif medium_button.collidepoint(mouse_pos):
                    return FPS_OPTIONS['medium']
                elif hard_button.collidepoint(mouse_pos):
                    return FPS_OPTIONS['hard']

        pygame.display.update()


def pause_menu(screen, current_fps):
    button_width, button_height = 100, 50
    button_spacing = 20
    resume_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - button_spacing, button_width, button_height)
    easy_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
    medium_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_height + button_spacing, button_width, button_height)
    hard_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 2 * (button_height + button_spacing), button_width, button_height)

    while True:
        screen.fill(BLACK)
        draw_text(screen, "Paused", (WIDTH // 2 - 50, HEIGHT // 2 - 150), WHITE)
        resume_draw_button(screen, "Resume", resume_button)
        draw_button(screen, "Easy", easy_button)
        draw_button(screen, "Medium", medium_button)
        draw_button(screen, "Hard", hard_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(mouse_pos):
                    return current_fps
                elif easy_button.collidepoint(mouse_pos):
                    return FPS_OPTIONS['easy']
                elif medium_button.collidepoint(mouse_pos):
                    return FPS_OPTIONS['medium']
                elif hard_button.collidepoint(mouse_pos):
                    return FPS_OPTIONS['hard']

        pygame.display.update()


def main():
    global SCREEN_HEIGHT
    SCREEN_HEIGHT = HEIGHT + HEADER_HEIGHT
    current_fps = start_screen(pygame.display.set_mode((WIDTH, SCREEN_HEIGHT), 0, 32))

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT), 0, 32)

    #game surface
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    game_surface = game_surface.convert()

    snake = Snake()
    food = Food()
    high_score = 0

    #button positions and sizes
    pause_button = pygame.Rect(WIDTH - 120, 10, 100, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                #Pause button click
                if pause_button.collidepoint(mouse_pos):
                    current_fps = pause_menu(screen, current_fps)  # Go to pause menu

        #Update snake position and check for collisions
        snake.update()
        if snake.get_head_position() == food.position:  # Collision check
            snake.length += 1
            snake.score += 1
            food.randomize_position()

            if snake.score > high_score:
                high_score = snake.score

        #Clear the game area
        game_surface.fill(WHITE)
        snake.render(game_surface)
        food.render(game_surface)
        #render the header
        screen.fill(BLACK)
        draw_text(screen, f"Record: {high_score}", (10, 10), WHITE)
        draw_text(screen, f"Score: {snake.score}", (10, 50), WHITE)
        resume_draw_button(screen, "Pause", pause_button)

        screen.blit(game_surface, (0, HEADER_HEIGHT))

        pygame.display.update()
        clock.tick(current_fps)

if __name__ == "__main__":
    main()
