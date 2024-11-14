import pygame
import math
from ai import AI

MAX_ANGLE_VELOCITY = 0.08
MAX_ACCELERATION = 0.25
FRICTION = 0.03  # 假设的摩擦系数，你需要根据实际情况进行调整
check_num = 0
CHECK_POINTS=["C","D","E","F"]
start_time = None
i= 0

class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """
    
    def __init__(self, controller):
        self.__has_finished = False
        self.controller = controller
        self.__position = [100, 100]  # Kart的初始位置
        self.__velocity = 0  # Kart的初始速度
        self.__angle = 0  # Kart的初始角度
        self.__angle_velocity = 0  # Kart的初始角速度
        self.__acceleration = 0  # Kart的初始加速度
        self.__check_p =  [0, 0, 0, 0] #设置chekpoint的初始值
        self.__next_checkpoint_id = 0
        self.__rebrithposition = [100, 100]
        self.__rebrithangle = 0
        self.__message_displayed = False
        self.__start_time = 0
        self.__game_start_time = pygame.time.get_ticks()
        #self.i = 0
        # 在控制器上设置kart属性指向当前的Kart实例
        # 这样做可以在AI类中通过controller访问Kart实例
        self.controller.kart = self

    # Utilise a AI
    @property
    def position(self):
        return self.__position
    # Utilise a AI
    @property
    def next_checkpoint_id(self):
        return self.__next_checkpoint_id
    # Utilise a AI
    @property
    def angle(self):
        return self.__angle

    # Utilise a Track
    @property
    def has_finished(self):
        return self.__has_finished



    def reset(self, initial_position, initial_orientation):
        # A completer
        self.__has_finished = False
        self.__position = initial_position
        self.__angle = initial_orientation
        self.__velocity = 0
        self.__angle_velocity = 0
        self.__acceleration = 0
        self.__check_p =  [0, 0, 0, 0]  #设置chekpoint的初始值
        self.__next_checkpoint_id = 0
        
    def forward(self):
        self.__acceleration += MAX_ACCELERATION
        

    def backward(self):
        self.__acceleration += -MAX_ACCELERATION
        

    def turn_left(self):
        self.__angle_velocity -= MAX_ANGLE_VELOCITY

    def turn_right(self):
        self.__angle_velocity += MAX_ANGLE_VELOCITY

    # def update_position(self, string, screen):
    def update_position(self, string, screen):
        print(self.__rebrithposition)
        x = int(self.__position[0] // 50)
        y = int(self.__position[1] // 50)
        rows = string.split('\n')
        if y > len(rows):
            y = len(rows)
        if y < 0:
            y = 0
        if x > len(rows[0]):
            x = len(rows[0])
        if x < 0:
            x = 0
            
        first_row = rows[y]
        actuel_str = first_row[x]

#%%  超出边界的判定        
        if (self.__position[0] < 1 or self.__position[0] > 1285 or self.__position[1] < 1 or self.__position[1] > 785):
            self.__position = self.__rebrithposition * 1
            self.__velocity = 0  # Kart的初始速度
            self.__angle = self.__rebrithangle
            self.__angle_velocity = 0  # Kart的初始角速度
            self.__acceleration = 0  # Kart的初始加速度
            # self.draw(screen)
                      
#%%胜利画面            
        elif self.__check_p[3] == 1:
            font = pygame.font.Font(None, 270)  # 创建字体对象
            text = font.render("Bravo", True, (255, 255, 255))  # 创建文本表面
            text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2 - 250))
            # text2 = font.render("Anniversaire", True, (255, 255, 255))  # 创建文本表面
            # text_rect2 = text.get_rect(center=(screen.get_width()/2 - 250, screen.get_height()/2 - 50))

            screen.fill((0, 0, 0)) 
            screen.blit(text, text_rect)  # 将文本绘制到屏幕上
            # screen.blit(text2, text_rect2)  # 将文本绘制到屏幕上

            # if self.i == 0:
            #     pygame.display.flip()  # 更新屏幕显示
            #     self.i = 1
            if self.__message_displayed == False:    # 这段代码用于在游戏结束后显示3s的bravo 然后结束游戏
                self.__message_displayed = True
                self.__start_time = pygame.time.get_ticks()  # 记录开始时间 只会记录一次
                # print(start_time)
            if self.__message_displayed == True:    #显示文字后,检测文字显示了多长时间
            
                times = pygame.time.get_ticks() # 这三行代码用于记录代码运行了多长时间
                times = (times - self.__game_start_time) / 1000
                
                if pygame.time.get_ticks() - self.__start_time > 3000 :
                    print(times)
                    self.__has_finished = True
            # self.draw(screen)
            # print(pygame.time.get_ticks() - self.start_time)
                
                 
#%%公路情况
        elif actuel_str == "R":
            
            self.__acceleration = self.__acceleration - FRICTION * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = self.__acceleration + self.__velocity * math.cos(self.__angle_velocity)

            
        
            # 根据速度和角度更新位置
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))

            self.__angle += math.degrees(self.__angle_velocity)  # 根据当前角速度更新角度
            self.__angle %= 360 # 保持角度在0到360度之间
            
            # 在每次更新后重置加速度和角速度，以便下次调用时不会再次应用
            self.__acceleration = 0
            self.__angle_velocity = 0
            
            # 绘制Kart的新位置
            
#%%草地情况            
        elif actuel_str == "G":
            self.__acceleration = self.__acceleration - 0.2 * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = self.__acceleration + self.__velocity * math.cos(self.__angle_velocity)
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))
            self.__angle += math.degrees(self.__angle_velocity)
            self.__angle %= 360
            self.__acceleration = 0
            self.__angle_velocity = 0
            
            
#%%岩浆情况        
        elif actuel_str == "L":
            self.__position = self.__rebrithposition * 1
            # self.angle = self.rebrithangle * 1
            self.__velocity = 0
            self.__acceleration = 0
            self.__angle_velocity = 0
            
#%%检查点情况        
        elif actuel_str in["C","D","E","F"]:            
            self.__acceleration = self.__acceleration - FRICTION * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = self.__acceleration + self.__velocity * math.cos(self.__angle_velocity)
            # 根据速度和角度更新位置
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))
            self.__angle += math.degrees(self.__angle_velocity)
            self.__angle %= 360
            self.__acceleration = 0
            self.__angle_velocity = 0
            
            # self.draw(screen)
            
            if actuel_str == "C" :
                if self.__check_p[0]==0:
                    self.__rebrithposition = 1 * self.__position
                self.__check_p[0] = 1
                self.__next_checkpoint_id = 1
                # self.rebrithposition = [367,160]
                self.__rebrithangle = self.__angle * 1
                
            if actuel_str == "D" and self.__check_p[0] == 1:  #判断是否经过了检查点C
                if self.__check_p[1] == 0:
                    self.__rebrithposition = self.__position * 1
                self.__check_p[1] = 1
                self.__next_checkpoint_id = 2
                self.__rebrithangle = self.__angle * 1
                
            if actuel_str == "E" and self.__check_p[1] == 1: #判断是否经过了检查点D
                if self.__check_p[2] == 0:
                    self.__rebrithposition = self.__position * 1
                self.__check_p[2] = 1
                self.__next_checkpoint_id = 3
                self.__rebrithangle = self.__angle * 1
                
            if actuel_str == "F" and self.__check_p[2] == 1: #判断是否经过了检查点E
                self.__check_p[3] = 1
                
#%%加速带情况         
        elif actuel_str == "B":
            self.__acceleration = self.__acceleration - FRICTION * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = 20
        
        
            # 根据速度和角度更新位置
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))

        
            # 根据当前角速度更新角度
            self.__angle += math.degrees(self.__angle_velocity)
            # 保持角度在0到360度之间
            self.__angle %= 360
            
            # 在每次更新后重置加速度和角速度，以便下次调用时不会再次应用
            self.__acceleration = 0
            self.__angle_velocity = 0
            
            # 绘制Kart的新位置
            
        else:
            pass

        
#%%画图函数    
    def draw(self, screen):
        
        size1 = 20
        size2 = 10
        
        #换一个三角形代表小车, 小车的顶角就是我们前进的方向
        top_point = (self.__position[0] + size1 * math.cos(math.radians(self.__angle)),
                     self.__position[1] + size1 * math.sin(math.radians(self.__angle)))
        left_point = (self.__position[0] + size2 * math.cos(math.radians(self.__angle + 120)),
                      self.__position[1] + size2 * math.sin(math.radians(self.__angle + 120)))
        right_point = (self.__position[0] + size2 * math.cos(math.radians(self.__angle + 240)),
                       self.__position[1] + size2 * math.sin(math.radians(self.__angle + 240)))


        pygame.draw.polygon(screen, (255, 255, 255), [top_point, left_point, right_point])
        
