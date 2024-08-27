import pygame
import sys
import random

pygame.init()

#constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
FPS = 10
HEADER_HEIGHT=50
SCREEN_HEIGHT = HEIGHT + HEADER_HEIGHT

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#font for the display
FONT = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score=0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % WIDTH), (cur[1] + (y*GRID_SIZE)) % HEIGHT)
        if new[1] < HEADER_HEIGHT:
            new = (new[0], HEADER_HEIGHT)
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
        self.score=0

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
                         random.randint(HEADER_HEIGHT // GRID_SIZE, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                         (self.position[0], self.position[1] - HEADER_HEIGHT, GRID_SIZE, GRID_SIZE))
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#function for display
def draw_text(surface, text, position, color=WHITE):
    text_surface = FONT.render(text, True, color)
    surface.blit(text_surface, position)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()
    high_score=0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != DOWN:
                        snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    if snake.direction != UP:
                        snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    if snake.direction != RIGHT:
                        snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    if snake.direction != LEFT:
                        snake.direction = RIGHT

        snake.update()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score+=1
            food.randomize_position()

            if snake.score>high_score:
                high_score=snake.score

        surface.fill(WHITE)
        snake.render(surface)
        food.render(surface)
        screen.fill(BLACK)
        # display the score and the record
        draw_text(screen, f"Score: {snake.score}", (10, 10),WHITE)
        draw_text(screen, f"Record: {high_score}", (WIDTH - 150, 10),WHITE)

        screen.blit(surface, (0, HEADER_HEIGHT))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
