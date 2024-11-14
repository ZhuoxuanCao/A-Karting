import math
import pygame
import time
import heapq
MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

    
class AI():
    
    def __init__(self,game_map):
        self.kart = None
        self.game_map = game_map.split("\n")
        self.__checkpoints = ['C', 'D', 'E', 'F']
        self.__flag = True
        self.__num_point = 0
        self.__path1 = (2, 2)
            
        
    # def set_kart(self, kart):
    #     self.kart = kart
        
        
    def get_neighbors(self, node):
        # directions = [(0, -1), (0, 1), (-1, 0), (1, 0),(-1,-1),(-1,1),(1,-1),(1,1)]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        neighbors = []
        x, y = node
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.game_map[0]) and 0 <= ny < len(self.game_map):
                # if self.game_map[ny][nx] == 'R' or self.game_map[ny][nx] in self.checkpoints or self.game_map[ny][nx] == 'B':
                neighbors.append((nx, ny))
        return neighbors


    # def heuristic(self, node, goal):
    #     return abs(node[0] - goal[0]) + abs(node[1] - goal[1]) #曼哈顿距离
    
    def heuristic(self, node, goal):
        return math.sqrt((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2)


    def distance(self, current, neighbor):
        # 这里定义的是每个邻居的成本
        #neighbor 是一个邻居的坐标
        x, y = neighbor
        
        terrain_type = self.game_map[y][x]
        # print(terrain_type)
        if terrain_type in ('R'):  
            return 1
        elif terrain_type in ('B'):  
            return 0.9
        elif terrain_type in ('G'):  
            return 3
        elif terrain_type in ('L'):  
            return float('inf')
        elif terrain_type in ('C','D','E','F'):
            return 1
        else:
            return float('inf')


    def find_checkpoint(self, char):
        #寻找检查点的坐标
        for y, row in enumerate(self.game_map):
            for x, col in enumerate(row):
                if col == char:
                    return (x, y)
        return None


    def search(self, start, goal):
        open_set = [] #初始化一个空列表 open_set 作为开放集合。在 A* 算法中，这个集合用来存储待评估的节点。
        heapq.heappush(open_set, (0, start)) #将起点加入开放集合。在这里，您使用了堆（优先队列）来存储节点，确保每次都能从中提取出具有最低 f 分数的节点。
        came_from = {} #初始化 came_from 字典，用于存储到达每个节点的最佳路径（其实是存储每个节点的前一个节点）
        g_score = {start: 0} #初始化 g_score 字典，记录从起点到每个节点的最短路径长度。起点的 g 分数设为 0。
        f_score = {start: self.heuristic(start, goal)} #初始化 f_score 字典，记录每个节点的 f 分数（即 g 分数加上启发式估计到终点的成本）。起点的 f 分数是其到终点的启发式估计成本。

        while open_set:
            current = heapq.heappop(open_set)[1] #从开放集合中取出具有最低 f 分数的节点作为当前节点。

            if current == goal: #如果当前节点是目标节点，则重建并返回从起点到目标点的路径。
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]


            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + self.distance(current, neighbor)
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        
        
        print("none")
        return None  # 如果找不到路径       
    
    
    def calcul_trace(self):
        # astar = AStar(map_string)

        start = (int(self.kart.position[0] // 50), int(self.kart.position[1] // 50))  # 起点
        print(f"now = {start}")
        full_path = [start]  # 初始化完整路径，包含起点

        for checkpoint in self.__checkpoints:
            goal = self.find_checkpoint(checkpoint)
            if goal:
                path = self.search(start, goal)
                if path:
                    full_path += path[1:]  # 添加路径，去除路径的第一个点（因为它是上一段路径的终点）
                    start = goal  # 更新下一个起点

        return full_path

    def move(self, string):
        time.sleep(0.01)
        # self.string = string.split("\n")
        if not self.kart:
            return {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        if self.__flag :
            self.__path1 = self.calcul_trace()
            # print(self.path1)
            self.__flag = True
        if self.kart.next_checkpoint_id == 0:
            self.__checkpoints = ['C', 'D', 'E', 'F']
            # self.checkpoints = ['C']
        if self.kart.next_checkpoint_id == 1:
            self.__checkpoints = ['D', 'E', 'F']
        if self.kart.next_checkpoint_id == 2:
            self.__checkpoints = ['E', 'F']
        if self.kart.next_checkpoint_id == 3:
            self.__checkpoints = ['F']
            
        # print(self.kart.next_checkpoint_id)
            
        """
        Cette methode contient une implementation d'IA tres basique.
        L'IA identifie la position du prochain checkpoint et se dirige dans sa direction.

        :param string: La chaine de caractere decrivant le circuit
        :param screen: L'affichage du jeu
        :param position: La position [x, y] actuelle du kartq
        :param angle: L'angle actuel du kart
        :param velocity: La vitesse [vx, vy] actuelle du kart
        :param next_checkpoint_id: Un entier indiquant le prochain checkpoint a atteindre
        :returns: un tableau de 4 boolean decrivant quelles touches [UP, DOWN, LEFT, RIGHT] activer
        """
        
        # =================================================
        # D'abord trouver la position du checkpoint
        # =================================================


        # On utilise x et y pour decrire les coordonnees dans la chaine de caractere
        # x indique le numero de colonne
        # y indique le numero de ligne
        
        
        if self.__num_point < len(self.__path1):
            x,y = self.__path1[self.__num_point]

        else:
            x,y=self.__path1[-1]
            print(0)

            
            
        print(f"next = {x},{y}")
        self.next_checkpoint_position = [x * BLOCK_SIZE + .5 * BLOCK_SIZE, y * BLOCK_SIZE + .5 * BLOCK_SIZE]
        # print(self.kart.position[0]//50,self.kart.position[0]//50)
        # print()
        if self.kart.position[0]//50 == x and self.kart.position[1]//50 == y:
            
            self.__num_point = 1
        print(self.__num_point)
        

        # =================================================
        # Ensuite, trouver l'angle vers le checkpoint
        # =================================================
        
        relative_x = self.next_checkpoint_position[0] - self.kart.position[0]
        relative_y = self.next_checkpoint_position[1] - self.kart.position[1]
        # print(relative_x,relative_y)
        
        # On utilise la fonction arctangente pour calculer l'angle du vecteur [relative_x, relative_y]
        next_checkpoint_angle = math.atan2(relative_y, relative_x)
        
        # L'angle relatif correspond a la rotation que doit faire le kart pour se trouver face au checkpoint
        # On applique l'operation (a + pi) % (2*pi) - pi pour obtenir un angle entre -pi et pi
        relative_angle = (next_checkpoint_angle - math.radians(self.kart.angle) + math.pi) % (2 * math.pi) - math.pi
        
        # =================================================
        # Enfin, commander le kart en fonction de l'angle
        # =================================================
        if relative_angle > MAX_ANGLE_VELOCITY:
            # On tourne a droite
            command = [False, False, False, True]
        elif relative_angle < -MAX_ANGLE_VELOCITY:
            # On tourne a gauche
            command = [False, False, True, False]
        else:
            # On avance
            command = [True, False, False, False]
            
        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        keys = {key: command[i] for i, key in enumerate(key_list)}
        return keys
    
    
    
