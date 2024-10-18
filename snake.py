import pygame, random

pygame.init()
screen = pygame.display.set_mode((800,800))
font = pygame.font.Font("freesansbold.ttf", 25)
clock = pygame.time.Clock()
running = True

counter = 0
snake = [(0,0)]
apple = (0,0)
# 0: not moving, 1-4 NESW
direction = 0

def move_apple():
    global apple
    done = False
    while not done:
        x = random.randint(0,19) * 40
        y = random.randint(0,19) * 40
        if (x,y) not in snake:
            apple = (x,y)
            done = True

def gradient(num):
    return 255 / num

move_apple()
score = 0

def has_duplicates(lst):
    seen = set()
    for item in lst:
        if item in seen:
            return True
        seen.add(item)
    return False

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
        if direction == 1: snake.append((cx,cy-40))
        if direction == 2: snake.append((cx+40,cy))
        if direction == 3: snake.append((cx,cy+40))
        if direction == 4: snake.append((cx-40,cy))
        if snake[-1][0] < 0: snake[-1] = (760, snake[-1][1])
        if snake[-1][0] > 760: snake[-1] = (0, snake[-1][1])
        if snake[-1][1] < 0: snake[-1] = (snake[-1][0], 760)
        if snake[-1][1] > 760: snake[-1] = (snake[-1][0], 0)
        if snake[-1] == apple: move_apple(); score += 1
    
        elif len(snake) > 4: snake.pop(0)
    green = 0
    for x,y in snake:
        pygame.draw.rect(screen, (0,int(green),0), pygame.Rect(x, y, 40, 40))
        green += gradient(len(snake))
    pygame.draw.rect(screen, (100,0,0), pygame.Rect(apple[0], apple[1], 40, 40))
    screen.blit(font.render(f"SCORE: {score}", False, (255,255,255)), (10,10))
    if has_duplicates(snake): running = False

    pygame.display.update()
pygame.quit()
