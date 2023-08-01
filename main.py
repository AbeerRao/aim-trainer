import random
import math
import time
import pygame


pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
LIVES = 30
BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR_MAIN = "red"
    COLOR_SECOND = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR_MAIN, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.COLOR_SECOND, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR_MAIN, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.COLOR_SECOND, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt(( self.x - x ) ** 2 + ( self.y - y ) ** 2)
        return dis <= self.size
    

def format_time(seconds):
    mili = math.floor(int(seconds * 1000 % 1000) / 100)
    secs = int(round(seconds % 60, 1))
    mins = int(seconds // 60)
    return f"{mins:02d}:{secs:02d}:{mili}"


def get_middle(surface):
    return (WIDTH / 2) - (surface.get_width() / 2)
    

def draw_top_bar(window, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(window, "grey", (0, 0, WIDTH, BAR_HEIGHT))
    speed = round(targets_pressed / elapsed_time, 1)

    time_label = LABEL_FONT.render(f"Time : {format_time(elapsed_time)}", 1, "black")
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits : {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives : {LIVES - misses}", 1, "black")
    window.blit(time_label, (5, 5))
    window.blit(speed_label, (200, 5))
    window.blit(hits_label, (450, 5))
    window.blit(lives_label, (650, 5))


def end_screen(window, elapsed_time, targets_pressed, clicks):
    window.fill(BG_COLOR)
    speed = round(targets_pressed / elapsed_time, 1)
    accuracy = round(targets_pressed/ clicks * 100, 1)

    time_label = LABEL_FONT.render(f"Time : {format_time(elapsed_time)}", 1, "white")
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits : {targets_pressed}", 1, "white")
    accouracy_label = LABEL_FONT.render(f"Accuracy : {accuracy}", 1, "white")
    window.blit(time_label, (get_middle(time_label), 100))
    window.blit(speed_label, (get_middle(speed_label), 200))
    window.blit(hits_label, (get_middle(hits_label), 300))
    window.blit(accouracy_label, (get_middle(accouracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
    

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()
    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(60)
        click = False
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, ( WIDTH - TARGET_PADDING ))
                y = random.randint(TARGET_PADDING + BAR_HEIGHT, ( HEIGHT - TARGET_PADDING ))
                target = Target(x, y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        for target in targets:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                misses += 1
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, target_pressed, clicks)
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()
    
    pygame.quit()


def draw(window, targets):
    window.fill(BG_COLOR)
    for target in targets:
        target.draw(window)


if __name__ == "__main__":
    main()