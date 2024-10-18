import pygame, random

pygame.init()
screen = pygame.display.set_mode((800,800))
font = pygame.font.Font("freesansbold.ttf", 25)
clock = pygame.time.Clock()
running = True

counter = 0
snake = [[0,0], [0,0]]
apple = [0,0]
# 0: not moving, 1-4 NESW
direction = 0

def move_apple():
    global apple
    done = False
    while not done:
        x = random.randint(0,20) * 40
        y = random.randint(0,20) * 40
        if [x,y] not in snake:
            apple = [x,y]
            done = True

move_apple()
score = 0

while running:
    dt = clock.tick(60)
    counter += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3: direction = 1
            if event.key == pygame.K_DOWN and direction != 1: direction = 3
            if event.key == pygame.K_RIGHT and direction != 4: direction = 2
            if event.key == pygame.K_LEFT and direction != 2: direction = 4

    screen.fill((0,0,0))

    if counter > 100:
        counter = 0
        cx,cy = snake[len(snake)-1]
        if direction == 1: snake.append([cx,cy-40])
        if direction == 1: snake.append([cx+40,cy])
        if direction == 3: snake.append([cx,cy+40])
        if direction == 4: snake.append([cx-40,cy])
        if snake[-1] == apple:
            move_apple()
        elif len(snake) > 4: snake.pop(0); score += 1

    for x,y in snake:
        pygame.draw.rect(screen, (0,100,0), pygame.Rect(x, y, 40, 40))
    pygame.draw.rect(screen, (100,0,0), pygame.Rect(apple[0], apple[1], 40, 40))
    screen.blit(font.render(f"SCORE: {score}", False, (255,255,255)), (10,10))

    pygame.display.update()
pygame.quit()
