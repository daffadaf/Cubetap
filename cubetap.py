import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CUBETAP")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 30
GRAVITY = 1
JUMP = -15
PIPE_WIDTH = 60
PIPE_GAP = 180

cube_img = pygame.Surface((30, 30))
cube_img.fill((255, 255, 0))

class Cube:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.vel = JUMP

    def draw(self, win):
        win.blit(cube_img, (self.x, self.y))

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= 5
        self.top.topleft = (self.x, 0)
        self.bottom.topleft = (self.x, self.height + PIPE_GAP)

    def draw(self, win):
        pygame.draw.rect(win, GREEN, self.top)
        pygame.draw.rect(win, GREEN, self.bottom)

def game_over(win, score):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    game_over_text = font_big.render("Game Over", True, BLACK)
    score_text = font_big.render(f"Score: {score}", True, BLACK)
    restart_text = font_small.render("Press any key to exit", True, BLACK)

    win.fill(WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()
    wait_for_exit()

def wait_for_exit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

def main():
    clock = pygame.time.Clock()
    run = True
    cube = Cube()
    pipes = [Pipe()]
    score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                cube.jump()

        cube.update()

        remove = []
        add_pipe = False
        for pipe in pipes:
            pipe.update()
            if pipe.x + PIPE_WIDTH < 0:
                remove.append(pipe)
                add_pipe = True
            if cube.rect.colliderect(pipe.top) or cube.rect.colliderect(pipe.bottom):
                game_over(win, score)
                run = False

        if cube.y > HEIGHT or cube.y < 0:
            game_over(win, score)
            run = False

        if add_pipe:
            score += 1
            pipes.append(Pipe())

        for r in remove:
            pipes.remove(r)

        win.fill(WHITE)
        cube.draw(win)
        for pipe in pipes:
            pipe.draw(win)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
