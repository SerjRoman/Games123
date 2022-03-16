import pygame
import os
import random 
import json

score_enemy = 0
flag_move_enemy = True
speed_enemy = 5


pygame.init()# Инициализирует все настройки pygame
display_width = 450
display_height = 520
game_window = pygame.display.set_mode((display_width,display_height))#Создаем окно с размером 300 и 600
pygame.display.set_caption("race")# Нызываем окно
list_car = []
list_map1 = [
            '202',
            '000',
            '020'
            ]
list_map2 = [
            '202',
            '002',
            '200'
            ]
list_map3 = [
            '022',
            '002',
            '200'
            ]
list_map4 = [
            '020',
            '002',
            '202'
            ]
list_map = [list_map1,list_map2,list_map3,list_map4]
def spawn_car():
    global speed_enemy
    X = 0
    Y = -450
    for el in list_map[random.randint(0,3)]:
        for el1 in el:
            if el1 == '2':
                car = Car(X,Y,speed_enemy,'car_enemy.png')
                list_car.append(car)
            X += 100
        X = 0
        Y += 150
flag_delete_cars = True
len_cars = 0
class Menu():
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.WIDTH = 450
        self.HEIGHT = 520
        self.menu_image = os.path.join(os.path.abspath(__file__+'/..'),'menu.png')
        self.menu_image = pygame.image.load(self.menu_image)
        self.menu_image = pygame.transform.scale(self.menu_image,(self.WIDTH,self.HEIGHT))

class Start_Game():
    def __init__(self):
        self.X = 175
        self.Y = 100
        self.WIDTH = 100
        self.HEIGHT = 50 
        self.start_image = os.path.join(os.path.abspath(__file__+'/..'),'start_game.png')
        self.start_image = pygame.image.load(self.start_image)
        self.start_image = pygame.transform.scale(self.start_image,(self.WIDTH,self.HEIGHT))

class Exit_Game():
    def __init__(self):
        self.X = 175
        self.Y = 200
        self.WIDTH = 100
        self.HEIGHT = 50 
        self.exit_image = os.path.join(os.path.abspath(__file__+'/..'),'exit_game.png')
        self.exit_image = pygame.image.load(self.exit_image)
        self.exit_image = pygame.transform.scale(self.exit_image,(self.WIDTH,self.HEIGHT))

class Car:#Класс игровых объектов 
    def __init__(self,x = 100,y = 390,speed = 5,name_image = 'car.png'):
        self.WIDTH = 100 # Статическая ширина 
        self.HEIGHT = 130 # Статическая высота
        self.X = x# координата х  
        self.Y = y# координата у
        self.Y2 = y
        self.IMAGE = os.path.join(os.path.abspath(__file__ + '/..'),name_image)# Получаем путь картинки 
        self.IMAGE = pygame.image.load(self.IMAGE)#Загружаем картинку 
        self.IMAGE = pygame.transform.scale(self.IMAGE,(self.WIDTH,self.HEIGHT))# Подстраиваем ширину и высоту нашего объекта
        self.SPEED = speed

    def move_enemy(self,el):
        global flag_move_enemy
        global flag_delete_cars
        global len_cars
        global score_enemy
        global speed_enemy
        if flag_move_enemy:
            if self.Y < display_height:
                self.Y = self.Y + self.SPEED
            else:
                if flag_delete_cars:
                    flag_delete_cars = False
                    len_cars = len(list_car)
                    spawn_car()
                if len_cars == 0:
                    flag_delete_cars = True
                self.Y = self.Y2
                x = list_car.index(el)
                del list_car[x]
                len_cars -= 1
                score_enemy += 1
                if score_enemy % 5 == 0:
                    speed_enemy += 1

    def collision(self,el):
        global flag_move_enemy
        if self.Y <= el.Y + 130 and self.Y - 130 < el.Y and self.X == el.X:
            flag_move_enemy = False

class Score():
    def __init__(self,screen,score_enemy,speed_enemy,score_high):
        self.screen = screen
        self.score_high = score_high
        self.speed_enemy = speed_enemy
        self.score_enemy = score_enemy
        self.screen_rect = screen.get_rect()
        self.text_color = (139,195,74)
        self.font = pygame.font.SysFont(None,36)
        self.image_score()
        self.image_speed()
        self.image_high_score()
    def image_score(self):
        self.score_image = self.font.render('Scores: '+str(self.score_enemy),True,self.text_color,(0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 25
        self.score_rect.top = 20
    def image_speed(self):
        self.speed_image = self.font.render('Speed: '+str(self.speed_enemy),True,self.text_color,(0,0,0))
        self.speed_rect = self.speed_image.get_rect()
        self.speed_rect.right = self.screen_rect.right - 25
        self.speed_rect.top = 60
    def image_high_score(self):
        self.high_score_image = self.font.render('H-Score: '+str(self.score_high),True,self.text_color,(0,0,0))
        self.hight_score_rect = self.score_image.get_rect()
        self.hight_score_rect.right = self.screen_rect.right - 25
        self.hight_score_rect.top = 100
    
def run_game():# Основная функция игры
    global list_car
    global flag_move_enemy
    global speed_enemy
    global score_enemy
    score_high = 0
    path = os.path.join(os.path.abspath(__file__+'/..'),'score_data.json')
    line = pygame.Surface((10,520))
    line.fill((0,0,0))
    game = True # Флаг работы игрового цикла
    player_car = Car()# Экземпляр класса car
    enemy_car = Car(100, 0, 0.5,'car_enemy.png')
    flag_move = True#Флаг движения
    menu = Menu()
    start_game = Start_Game()
    exit_game = Exit_Game()
    fps = pygame.time.Clock()
    flag_menu = False
    if os.path.isfile(path):
        with open('score_data.json','r') as file:
            score_high = json.load(file)
            score_high = score_high['SCORE']
    while game:#Игровой цикл
        if flag_menu:
            scores = Score(game_window,score_enemy,speed_enemy,score_high)
            speed_stat = Score(game_window,score_enemy,speed_enemy,score_high)
            if os.path.isfile(path) and flag_move_enemy:
                high_score = Score(game_window,score_enemy,speed_enemy,score_high)
            game_window.fill((125,125,125))#Заливаем фон окна серым цветом
            game_window.blit(line,(300,0))
            game_window.blit(player_car.IMAGE,(player_car.X,player_car.Y))#Отрисовывем на экране необходимый объект 
            # game_window.blit(enemy_car.IMAGE,(enemy_car.X,enemy_car.Y))
            # enemy_car.move_enemy()
            if flag_move_enemy:

                for el in list_car:
                    game_window.blit(el.IMAGE,(el.X,el.Y))
                    el.move_enemy(el)
                    player_car.collision(el)
                    if flag_move_enemy == False:
                        flag_menu = False
                        print('Дотронулся')
                        if score_high <= score_enemy:
                            flag_menu = False
                            stat_data = {'SCORE':score_enemy}
                            with open('score_data.json','w') as file:
                                json.dump(stat_data,file)  
                            flag_menu = False
                keys = pygame.key.get_pressed()#Записываем в перменную список всех нажатий на клавиши 
                if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:# Если клавиши обе не нажаты то задаем значение нашего флага на True
                    flag_move = True
                if keys[pygame.K_LEFT] and player_car.X > 0 and flag_move:#Проверяем нажатие на клавишу влево и двигаем если флаг True
                    player_car.X -= 100
                    flag_move = False
                    print('Нажал лево')
                if keys[pygame.K_RIGHT] and player_car.X <200 and flag_move:#Проверяем нажатие на клавишу вправо и двигаем если флаг True
                    player_car.X += 100
                    flag_move = False
                    print('Нажал право')
                
            game_window.blit(scores.score_image,scores.score_rect)
            game_window.blit(speed_stat.speed_image,speed_stat.speed_rect)
            if os.path.isfile(path) and flag_move_enemy:
                game_window.blit(high_score.high_score_image,high_score.hight_score_rect)
        if flag_menu == False:
            speed_enemy = 5
            game_window.blit(menu.menu_image,(menu.X,menu.Y))   
            game_window.blit(start_game.start_image,(start_game.X,start_game.Y))
            game_window.blit(exit_game.exit_image,(exit_game.X,exit_game.Y))
            pressed_mouse = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            if pressed_mouse[0] == True and pos[0] >= start_game.X and pos[0] <= start_game.X+start_game.WIDTH and pos[1] >= start_game.Y and pos[1] <= start_game.Y+start_game.HEIGHT:
                list_car = []
                spawn_car()
                score_enemy = 0
                flag_move_enemy = True
                speed_enemy = 5
                flag_menu = True
                flag_move_enemy = True
                player_car = Car()# Экземпляр класса car
                if os.path.isfile(path):
                    with open('score_data.json','r') as file:
                        score_high = json.load(file)
                        score_high = score_high['SCORE']
            if pressed_mouse[0] == True and pos[0] >= exit_game.X and pos[0] <= exit_game.X+exit_game.WIDTH and pos[1] >= exit_game.Y and pos[1] <= exit_game.Y+exit_game.HEIGHT:
                game = False
            
        for event in pygame.event.get():# Создаем цикл и записываем в event все события 
            if event.type == pygame.QUIT:#Проверяем если нажат крестик, то меняем игровой флаг на False
                game = False
        pygame.display.flip()# Перерисовывает экран     
        fps.tick(30)



run_game()# Вызываем фукнцию






































