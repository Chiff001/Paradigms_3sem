from game import Game, Snake, Food, Border
import pygame


nik = 'tasher'
# Легкий
# Средний
# Сложный
# Эксперт
lvl = "Средний"
game = Game(lvl, nik)
snake = Snake(game.green, game.x0, game.y0)
food = Food(game.x0, game.y0, game.screen_width, game.screen_height, game.a, snake.snake_body)
all_sprites = pygame.sprite.Group()
Border(game.x0, game.y0, game.screen_width, game.y0, all_sprites)
Border(game.x0, game.screen_height, game.screen_width, game.screen_height, all_sprites)
Border(game.x0, game.y0, game.x0, game.screen_height, all_sprites)
Border(game.screen_width, game.y0, game.screen_width, game.screen_height, all_sprites)
while game.run:
    snake.change = game.events(snake.change) # Задаем направление
    snake.change_direction() # Проверка на изменение направления движения
    snake.move() # Меняем направление движения
    game.score, food.food_pos, game.speed, food.type = snake.check_food(
    game.score, food.food_pos, game.x0, game.y0, game.screen_width, game.screen_height,
    game.lvl, game.speed, food.type, game.a) # Получаем количество очков, новую позицию еды, скорость и тип еды
    if snake.check_on_crash(
        game.game_over, game.x0, game.y0, game.screen_width, game.screen_height, game.a): # Проверка на столкновение
        snake.draw_snake(game.screen, game.white) # Прорисовываем заново змейку
        food.draw_food(game.screen, lvl) # Прорсовываем еду
        all_sprites.draw(game.screen) # Прорисовка стен игрого поля
        all_sprites.update()
        game.boxes() # Прорисовка препятствий
        game.show_score() # Показываем количество очков
        game.snake_speed() # Обновляем показатели скорости