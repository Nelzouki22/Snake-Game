# استيراد المكتبات
import pygame
import time
import random
import math

# تهيئة مكتبة Pygame
pygame.init()

# سرعة الثعبان
snake_speed = 15

# حجم نافذة اللعبة
window_x = 720
window_y = 480

# تعريف الألوان
black = pygame.Color(0, 0, 0)  # اللون الأسود
white = pygame.Color(255, 255, 255)  # اللون الأبيض
red = pygame.Color(255, 0, 0)  # اللون الأحمر
green = pygame.Color(0, 255, 0)  # اللون الأخضر
blue = pygame.Color(0, 0, 255)  # اللون الأزرق

# إنشاء نافذة اللعبة
pygame.display.set_caption('لعبة الثعبان مع المطارد')
game_window = pygame.display.set_mode((window_x, window_y))

# التحكم في معدل الإطارات (frames per second)
fps = pygame.time.Clock()

# تحديد الموقع الافتراضي للثعبان
snake_position = [100, 50]

# تحديد أول 4 كتل من جسم الثعبان
snake_body = [[100, 50], 
              [90, 50], 
              [80, 50], 
              [70, 50]]

# موقع الفاكهة
fruit_position = [random.randrange(1, (window_x // 10)) * 10, 
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# تحديد الموقع الأولي للمطارد (العدو)
chaser_position = [random.randrange(1, (window_x // 10)) * 10, 
                   random.randrange(1, (window_y // 10)) * 10]

# تحديد الاتجاه الافتراضي للثعبان
direction = 'RIGHT'
change_to = direction

# تحديد النقاط الابتدائية
score = 0

# دالة لعرض النقاط
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('النقاط : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_x / 10, 15)
    else:
        score_rect.midtop = (window_x / 2, window_y / 1.25)
    game_window.blit(score_surface, score_rect)

# دالة لإنهاء اللعبة
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        'نقاطك هي : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# دالة لتحريك المطارد باتجاه الثعبان
def move_chaser(chaser_pos, snake_pos):
    chaser_speed = 10  # سرعة المطارد
    dx = snake_pos[0] - chaser_pos[0]
    dy = snake_pos[1] - chaser_pos[1]
    distance = math.hypot(dx, dy)
    
    if distance == 0:
        return chaser_pos
    
    # حساب الاتجاه وتحريك المطارد
    dx /= distance
    dy /= distance
    
    chaser_pos[0] += dx * chaser_speed
    chaser_pos[1] += dy * chaser_speed
    
    return chaser_pos

# منطق اللعبة الرئيسي
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not change_to == 'DOWN':
                    change_to = 'UP'
            if event.key == pygame.K_DOWN:
                if not change_to == 'UP':
                    change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                if not change_to == 'RIGHT':
                    change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                if not change_to == 'LEFT':
                    change_to = 'RIGHT'

    # تحديث اتجاه حركة الثعبان بناءً على الإدخال
    if change_to == 'UP':
        direction = 'UP'
    if change_to == 'DOWN':
        direction = 'DOWN'
    if change_to == 'LEFT':
        direction = 'LEFT'
    if change_to == 'RIGHT':
        direction = 'RIGHT'

    # تحريك الثعبان
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # آلية زيادة طول جسم الثعبان
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    # توليد الفاكهة في مكان عشوائي بعد أن يأكلها الثعبان
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    # رسم جسم الثعبان
    for pos in snake_body:
        pygame.draw.rect(game_window, red, pygame.Rect(
            pos[0], pos[1], 10, 10))

    # رسم الفاكهة
    pygame.draw.rect(game_window, green, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # تحريك المطارد ورسمه
    chaser_position = move_chaser(chaser_position, snake_position)
    pygame.draw.rect(game_window, blue, pygame.Rect(
        chaser_position[0], chaser_position[1], 10, 10))

    # شروط إنهاء اللعبة إذا اصطدم الثعبان بالجدار
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    # التحقق من اصطدام الثعبان بجسمه
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    # التحقق من اقتراب المطارد من الثعبان
    if math.hypot(snake_position[0] - chaser_position[0], snake_position[1] - chaser_position[1]) < 10:
        game_over()

    # عرض النقاط بشكل مستمر
    show_score(1, white, 'times new roman', 20)

    # تحديث شاشة اللعبة
    pygame.display.update()

    # معدل الإطارات لكل ثانية (التحكم في سرعة اللعبة)
    fps.tick(snake_speed)

