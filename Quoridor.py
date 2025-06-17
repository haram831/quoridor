import pygame

pygame.init()

#size
CELL_SIZE = 10
BLOCK_SIZE = 5
OBSTACLE_SIZE = 11
#number
BLOCK_NUM = 9
OBSTACLE_NUM = BLOCK_NUM + 1
#state
EMPTY = 0
SELECT = 1
FILL = 2
RED = 4
WHITE = 5

UNUSED = 0
USED = 1

NOTHING_SELECTED=0
PIECE_SELECTED=1
OBSTACLE_SELECTED=2

#shape type
VERTICAL = 0
HORIZONAL = 1
CROSSING = 2

COLOR = {'LIGHT_BROWN':(196,154,108), 'DARK_BROWN':(60,36,21),
         'RED_BROWN':(111,21,41), 'BROWN':(139,94,60),
         'ASHE_BROWN':(194,181,155), 'WHITE':(241,242,242),
         'BLACK':(0,0,0), 'RED':(150,0,24)}

BLOCK_SELECT = pygame.Surface([CELL_SIZE*BLOCK_SIZE, CELL_SIZE*BLOCK_SIZE], pygame.SRCALPHA)
pygame.draw.circle(BLOCK_SELECT, COLOR['WHITE'], [CELL_SIZE*BLOCK_SIZE//2, CELL_SIZE*BLOCK_SIZE//2], CELL_SIZE*BLOCK_SIZE//5)
BLOCK_SELECT.set_alpha(100)

OBSTACLE = pygame.Surface([CELL_SIZE, CELL_SIZE*OBSTACLE_SIZE], pygame.SRCALPHA)
pygame.draw.rect(OBSTACLE, COLOR['LIGHT_BROWN'], [0, 0, CELL_SIZE, CELL_SIZE*OBSTACLE_SIZE], 0)

PLAYER_WHITE = pygame.image.load(r"C:\Users\gim22\OneDrive\바탕 화면\quoridor\quoridor_white.png")
PLAYER_WHITE = pygame.transform.scale(PLAYER_WHITE, (CELL_SIZE*2, CELL_SIZE*4))
PLAYER_RED = pygame.image.load(r"C:\Users\gim22\OneDrive\바탕 화면\quoridor\quoridor_red.png")
PLAYER_RED = pygame.transform.scale(PLAYER_RED, (CELL_SIZE*2, CELL_SIZE*4))

FONT = pygame.font.SysFont(None, 90)
FONT_HALF = pygame.font.SysFont(None, 30)

class BLOCK:
    def __init__(self, window, x, y, color=COLOR['BROWN']):
        self.window = window
        self.color = color
        self.x = x
        self.y = y
        #EMPTY, RED, WHITE, SELECT
        self.state = EMPTY
        self.x_pos = CELL_SIZE*(1 + self.x//2*(OBSTACLE_SIZE-BLOCK_SIZE))
        self.y_pos = CELL_SIZE*self.y//2*(OBSTACLE_SIZE-BLOCK_SIZE)
        self.size = BLOCK_SIZE*CELL_SIZE
        
    def draw(self):
        pygame.draw.rect(self.window, self.color, [self.x_pos, self.y_pos, self.size, self.size])
        if self.state == SELECT:
            self.window.blit(BLOCK_SELECT,(self.x_pos,self.y_pos))
        elif self.state == WHITE:
            self.window.blit(PLAYER_WHITE, (self.x_pos + (self.size-PLAYER_WHITE.get_rect().size[0])//2, self.y_pos + CELL_SIZE//2))
        elif self.state == RED:
            self.window.blit(PLAYER_RED, (self.x_pos + (self.size-PLAYER_WHITE.get_rect().size[0])//2, self.y_pos + CELL_SIZE//2))
            
    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def contain(self, x_pos, y_pos):
        return self.x_pos <= x_pos < self.x_pos + self.size and self.y_pos <= y_pos < self.y_pos + self.size
    
    def set_color(self, color):
        self.color = color
    
class ROAD:
    def __init__(self, window, x, y, shape_type, width, height, color=COLOR['DARK_BROWN']):
        self.window = window
        #EMPTY, FILL
        self.state = EMPTY
        #VERTICAL, HORIZONAL, CROSSING
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.x_pos = 0
        self.y_pos = 0
        
        self.set_pos()
    
    def set_pos(self):
        if self.shape_type == VERTICAL:
            self.x_pos = self.x//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
            self.y_pos = self.y//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
        elif self.shape_type == HORIZONAL:
            self.x_pos = CELL_SIZE*(1+ self.x//2*(OBSTACLE_SIZE-BLOCK_SIZE))
            self.y_pos = CELL_SIZE*(BLOCK_SIZE+self.y//2*(OBSTACLE_SIZE-BLOCK_SIZE))
        elif self.shape_type == CROSSING:
            self.x_pos = self.x//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
            self.y_pos = CELL_SIZE*(BLOCK_SIZE+self.y//2*(OBSTACLE_SIZE-BLOCK_SIZE))
        
    def draw(self):
        pygame.draw.rect(self.window, self.color, [self.x_pos, self.y_pos, self.width, self.height], 0)
            
    def set_state(self,state):
        self.state = state
        
    def get_shape_type(self):
        return self.shape_type
        
    def get_state(self):
        return self.state
    
    def contain(self, x_pos, y_pos):
        return self.x_pos <= x_pos < self.x_pos+self.width and self.y_pos <= y_pos < self.y_pos+self.height 

class OBSTACLES:
    def __init__(self, window, x, y, orgin_x, orgin_y, shape_type):
        self.window = window
        #USED, UNUSED, SELECT
        self.state = UNUSED
        #VERTICAL, HORIZONAL
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.x_pos = 0
        self.y_pos = 0
        self.width = 0
        self.height = 0
        self.orgin_x = orgin_x
        self.orgin_y = orgin_y
        
        self.set_size()
        self.set_pos(x, y)
        
    def draw(self):
        if self.shape_type == VERTICAL:
            self.window.blit(OBSTACLE, (self.x_pos, self.y_pos))
        elif self.shape_type == HORIZONAL:
            OBSTACLE_HORIZONAL = pygame.transform.rotate(OBSTACLE, 90)
            self.window.blit(OBSTACLE_HORIZONAL, (self.x_pos, self.y_pos))
            
    def set_state(self,state):
        self.state = state
        
    def set_shape_type(self, shape_type):
        self.shape_type = shape_type
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        if self.shape_type == VERTICAL:
            self.x_pos = self.x//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
            self.y_pos = self.y//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
        elif self.shape_type == HORIZONAL:
            self.x_pos = CELL_SIZE*(1+ self.x//2*(OBSTACLE_SIZE-BLOCK_SIZE))
            self.y_pos = CELL_SIZE*(BLOCK_SIZE + self.y//2*(OBSTACLE_SIZE-BLOCK_SIZE))
        
    def set_size(self):
        if self.shape_type == VERTICAL:
            self.width = CELL_SIZE
            self.height = CELL_SIZE*OBSTACLE_SIZE
        elif self.shape_type == HORIZONAL:
            self.width = CELL_SIZE*OBSTACLE_SIZE
            self.height = CELL_SIZE
    
    def get_shape_type(self):
        return self.shape_type
    
    def get_index(self):
        return self.x, self.y
    
    def get_pos(self):
        return self.x_pos, self.y_pos
    
    def get_orgin(self):
        return self.orgin_x, self.orgin_y
    
    def get_state(self):
        return self.state
            
    def contain(self, x_pos, y_pos):
        return self.x_pos <= x_pos < self.x_pos + self.width and self.y_pos <= y_pos < self.y_pos + self.height
    
    def complement(self):
        if self.state == UNUSED:
            return USED
        else:
            return UNUSED
        
    
class BOARD:
    def __init__(self, BOARD_ROW_NUM = (BLOCK_NUM+4)*BLOCK_SIZE + OBSTACLE_NUM+2, BOARD_COLUMN_NUM = BLOCK_NUM*BLOCK_SIZE + OBSTACLE_NUM):
        self.BOARD = []
        self.BOARD_ROW_NUM = BOARD_ROW_NUM
        self.BOARD_COLUMN_NUM = BOARD_COLUMN_NUM
        self.BOARD_WIDTH = self.BOARD_COLUMN_NUM*CELL_SIZE
        self.BOARD_HEIGHT = self.BOARD_ROW_NUM*CELL_SIZE
        self.window = pygame.display.set_mode([self.BOARD_WIDTH, self.BOARD_HEIGHT])
        self.OBSTACLES = []
        
    def set_board(self):
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            row = []
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if y % 2 == 0:
                    if x % 2 == 0:
                        row.append(ROAD(self.window, x, y, VERTICAL, CELL_SIZE, CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)))
                    else:
                        row.append(BLOCK(self.window, x, y))
                else:
                    if x % 2 == 0:
                        row.append(ROAD(self.window, x, y, CROSSING, CELL_SIZE, CELL_SIZE))
                    else:
                        if y == 1 or y == BLOCK_NUM + OBSTACLE_NUM  + 4:
                            row.append(ROAD(self.window, x, y, HORIZONAL, CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE), CELL_SIZE, COLOR['BROWN']))
                        else:
                            row.append(ROAD(self.window, x, y, HORIZONAL, CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE), CELL_SIZE))
            self.BOARD.append(row)

    def initialize_obstacle(self):
        self.OBSTACLES = []
        for y in [0, BLOCK_NUM + OBSTACLE_NUM+3]:
            row = []
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if x%2==0:
                    row.append(OBSTACLES(self.window, x, y, x, y, VERTICAL))
            # [0][] -> red, [1][] -> white
            self.OBSTACLES.append(row)

    def initialize_board(self):
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                self.BOARD[y][x].set_state(EMPTY)
        for y in range(3):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if x%2==0:
                    self.BOARD[y][x].set_state(FILL)
                    self.BOARD[BLOCK_NUM + OBSTACLE_NUM + 5 -y][x].set_state(FILL)
        self.BOARD[4][(BLOCK_NUM + OBSTACLE_NUM)//2].set_state(RED)
        self.BOARD[BLOCK_NUM + OBSTACLE_NUM + 1][(BLOCK_NUM + OBSTACLE_NUM)//2].set_state(WHITE)
        self.set_select_block(WHITE)
        
    def set_select_block(self, player):
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if self.BOARD[y][x].get_state()==player and isinstance(self.BOARD[y][x], BLOCK):
                    for dy,dx in (-2, 0), (2, 0), (0, -2), (0, 2):
                        if self.valid_block(x+dx, y+dy, player) and self.BOARD[y+dy//2][x+dx//2].get_state() == EMPTY:
                            if self.BOARD[y+dy][x+dx].get_state()==EMPTY:
                                self.BOARD[y+dy][x+dx].set_state(SELECT)
                            if self.BOARD[y+dy][x+dx].get_state()==self.complement(player):
                                if self.valid_road(x+(dx//2*3), y+(dy//2*3)) and self.BOARD[y+(dy//2*3)][x+(dx//2*3)].get_state()==EMPTY:
                                    if self.valid_block(x+(dx*2), y+(dy*2), player) and self.BOARD[y+(dy*2)][x+(dx*2)].get_state()==EMPTY:
                                        self.BOARD[y+(dy*2)][x+(dx*2)].set_state(SELECT)
                                elif self.valid_road(x+(dx//2*3), y+(dy//2*3)) and self.BOARD[y+(dy//2*3)][x+(dx//2*3)].get_state()==FILL:
                                    if self.BOARD[y+(dy//2*3)][x+(dx//2*3)].get_shape_type()==HORIZONAL:
                                        if self.valid_block(x+dx-2 , y+dy, player) and self.BOARD[y+dy][x+dx-2].get_state()==EMPTY:
                                            if self.BOARD[y+dy//2][x+dx-2].get_state()==EMPTY:
                                                self.BOARD[y+dy][x+dx-2].set_state(SELECT)
                                        if self.valid_block(x+dx+2 , y+dy, player) and self.BOARD[y+dy][x+dx+2].get_state()==EMPTY:
                                            if self.BOARD[y+dy//2][x+dx+2].get_state()==EMPTY:
                                                self.BOARD[y+dy][x+dx+2].set_state(SELECT)
                                                
                                    elif self.BOARD[y+(dy//2*3)][x+(dx//2*3)].get_shape_type()==VERTICAL:
                                        if self.valid_block(x+dx , y+dy-2, player) and self.BOARD[y+dy-2][x+dx].get_state()==EMPTY:
                                            if self.BOARD[y+dy-2][x+dx//2].get_state()==EMPTY:
                                                self.BOARD[y+dy-2][x+dx].set_state(SELECT)
                                        if self.valid_block(x+dx , y+dy+2, player) and self.BOARD[y+dy+2][x+dx].get_state()==EMPTY:
                                            if self.BOARD[y+dy+2][x+dx//2].get_state()==EMPTY:
                                                self.BOARD[y+dy+2][x+dx].set_state(SELECT)
                            
                        
    def valid_block(self, x, y, player):
        if player == RED:
            return 1 <= x <= 17 and 4 <= y <= 22
        if player == WHITE:
            return 1 <= x <= 17 and 2 <= y <= 20
        
    def valid_road(self, x, y):
        return 0 <= x < BLOCK_NUM + OBSTACLE_NUM and 3 <= y < BLOCK_NUM + OBSTACLE_NUM + 3
    
    def clean_block(self):
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if isinstance(self.BOARD[y][x], BLOCK) and self.BOARD[y][x].get_state() == SELECT:
                    self.BOARD[y][x].set_state(EMPTY)
                    
    def clean_board(self):
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if isinstance(self.BOARD[y][x], ROAD) and self.BOARD[y][x].get_state() == FILL:
                    self.BOARD[y][x].set_state(EMPTY)
        self.clean_block()
                    
    def update(self):
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                self.BOARD[y][x].draw()
        for obstacles in self.OBSTACLES:
            for obstacle in obstacles:
                obstacle.draw()
        
        
    def check_overlapping_obstacle(self, x, y):
        if self.BOARD[y][x].get_shape_type() == HORIZONAL:
            # 가로 장애물일 경우, 현재 위치와 오른쪽 두 칸을 검사
            if (self.valid_road(x, y) and self.valid_road(x+1, y) and self.valid_road(x+2, y)):
                if (self.BOARD[y][x].get_state() == EMPTY and
                    self.BOARD[y][x+1].get_state() == EMPTY and
                    self.BOARD[y][x+2].get_state() == EMPTY):
                    return False
        elif self.BOARD[y][x].get_shape_type() == VERTICAL:
            # 세로 장애물일 경우, 현재 위치와 아래쪽 두 칸을 검사
            if (self.valid_road(x, y) and self.valid_road(x, y+1) and self.valid_road(x, y+2)):
                if (self.BOARD[y][x].get_state() == EMPTY and
                    self.BOARD[y+1][x].get_state() == EMPTY and
                    self.BOARD[y+2][x].get_state() == EMPTY):
                    return False
        return True

    
    # def DFS(self, x, y, player):
    #     if player == WHITE:
    #         if y==2:
    #             return True
    #     if player == RED:
    #         if y==self.BOARD_ROW_NUM-3:
    #             return True
    #     for dy,dx in (-1,0), (1,0), (0,1), (0,-1):
    #         if self.valid_road(x+dx, y+dy):
    #             if self.BOARD[y+dy][x+dx].get_state()==EMPTY and isinstance(self.BOARD[y+dy][x+dx], ROAD):
    #                 if self.valid_block(x+dx*2, y+dy*2):
    #                     self.DFS(x+dx*2, y+dy*2, player)
    
    def DFS(self, x, y, player):
        stack = [(x, y)]
        visited = set()
    
        while stack:
            current_x, current_y = stack.pop()
            if (current_x, current_y) in visited:
                continue
            visited.add((current_x, current_y))
            if player == WHITE and current_y == 2:
                return True
            if player == RED and current_y == 22:
                return True
    
            for dy, dx in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                next_x = current_x + dx * 2
                next_y = current_y + dy * 2
    
                if self.valid_road(current_x + dx, current_y + dy):
                    if self.BOARD[current_y + dy][current_x + dx].get_state() == EMPTY and isinstance(self.BOARD[current_y + dy][current_x + dx], ROAD):
                        if self.valid_block(next_x, next_y, player) and (next_x, next_y) not in visited:
                            stack.append((next_x, next_y))
        return False
                        
    def get_click_event(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    raise
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    yield mouse_x, mouse_y
                        
    def check_winner(self):
        for x in range(BLOCK_NUM + OBSTACLE_NUM):
            if x%2 == 1 and isinstance(self.BOARD[2][x], BLOCK):
                if self.BOARD[2][x].get_state() == WHITE:
                    return WHITE
        for x in range(BLOCK_NUM + OBSTACLE_NUM):
            if x%2 == 1 and isinstance(self.BOARD[BLOCK_NUM + OBSTACLE_NUM + 3][x], BLOCK):
                if self.BOARD[BLOCK_NUM + OBSTACLE_NUM + 3][x].get_state() == RED:
                    return RED
        return None
                    
    def complement(self, player):
        assert player in [WHITE, RED]
        if player == WHITE:
            return RED
        if player == RED:
            return WHITE
        
    def print_turn(self, player):
        if player == RED:
            turn_text = FONT_HALF.render('Player: Red', True, COLOR['RED'])
        elif player == WHITE:
            turn_text = FONT_HALF.render('Player: WHITE', True, COLOR['WHITE'])
            
        self.window.blit(turn_text, [CELL_SIZE*2, CELL_SIZE])
                    
    def play(self): 
        turn_change = False
        state = NOTHING_SELECTED
        player = WHITE
        selected_object = None
        winner = None
        self.set_board()
        self.initialize_board()
        self.initialize_obstacle()
        self.update()
        self.print_turn(player)
        
        while True:
            self.print_turn(player)
            if state == NOTHING_SELECTED:
                self.set_select_block(player)
                self.update()
                self.print_turn(player)
                pygame.display.flip()
                state, selected_object = self.NOTHING_SELECTED(player)
            if state == PIECE_SELECTED:
                state, selected_object, turn_change = self.PIECE_SELECTED(player, selected_object)
                self.clean_block()
                if state == NOTHING_SELECTED and turn_change:
                    winner = self.check_winner()
                    if winner:
                        return winner
                    player = self.complement(player)
            if state == OBSTACLE_SELECTED:
                self.clean_block()
                self.update()
                self.print_turn(player)
                pygame.display.flip()
                state, selected_object, turn_change = self.OBSTACLE_SELECTED(player, selected_object)
                if state == NOTHING_SELECTED and turn_change:
                    winner = self.check_winner()
                    if winner:
                        return winner
                    player = self.complement(player)
                    print('trun change')
        
    def NOTHING_SELECTED(self, player):
        click_event_gen = self.get_click_event()
        click_x, click_y = next(click_event_gen)
        for obstacle in self.OBSTACLES[player-4]:
            if obstacle.contain(click_x, click_y):
                selected_object = obstacle
                return OBSTACLE_SELECTED, selected_object
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if self.BOARD[y][x].contain(click_x, click_y) and isinstance(self.BOARD[y][x], BLOCK):
                    if self.BOARD[y][x].get_state() == player:
                        selected_object = self.BOARD[y][x]
                        selected_object.set_color(COLOR['LIGHT_BROWN'])
                        self.update()
                        self.print_turn(player)
                        pygame.display.flip()
                        return PIECE_SELECTED, selected_object
        return NOTHING_SELECTED, None
                        
    def PIECE_SELECTED(self, player, selected_object):
        click_event_gen = self.get_click_event()
        click_x, click_y = next(click_event_gen)
        for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
            for x in range(BLOCK_NUM + OBSTACLE_NUM):
                if self.BOARD[y][x].contain(click_x, click_y) and isinstance(self.BOARD[y][x], BLOCK):
                    if self.BOARD[y][x] == selected_object:
                        selected_object.set_color(COLOR['BROWN'])
                        return NOTHING_SELECTED, None, False
                    if self.BOARD[y][x].get_state() == SELECT:
                        selected_object.set_state(EMPTY)
                        selected_object.set_color(COLOR['BROWN'])
                        self.BOARD[y][x].set_state(player)
                        self.update()
                        self.print_turn(player)
                        pygame.display.flip()
                        return NOTHING_SELECTED, None, True
        return NOTHING_SELECTED, None, False
    
    def OBSTACLE_SELECTED(self, player, selected_object):
        orgin_x, orgin_y = selected_object.get_orgin()
        orgin_xpos = orgin_x//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
        orgin_ypos = orgin_y//2*CELL_SIZE*(OBSTACLE_SIZE-BLOCK_SIZE)
        
        while True:
            events = pygame.event.get()
            
            # 모션 이벤트 처리
            for event in events:
                if event.type == pygame.QUIT:
                    raise
                    
                if event.type == pygame.MOUSEMOTION:
                    motion_x, motion_y = event.pos                    
                    for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
                        for x in range(BLOCK_NUM + OBSTACLE_NUM):
                            if self.BOARD[y][x].contain(motion_x, motion_y) and isinstance(self.BOARD[y][x], ROAD):
                                if self.valid_road(x, y):
                                    if selected_object.get_state() == UNUSED:
                                        if self.BOARD[y][x].get_shape_type() == VERTICAL:
                                            if self.valid_road(x, y+2):
                                                selected_object.set_shape_type(VERTICAL)
                                                selected_object.set_pos(x, y)
                                        elif self.BOARD[y][x].get_shape_type() == HORIZONAL:
                                            if self.valid_road(x+2, y):
                                                selected_object.set_shape_type(HORIZONAL)
                                                selected_object.set_pos(x, y)
                                        self.update()
                                        self.print_turn(player)
                                        pygame.display.flip()
                                        break  # 다음 이벤트 처리로 넘어감
                                    else:
                                        return NOTHING_SELECTED, None, False

            # 클릭 이벤트 처리     
                index_x, index_y = selected_object.get_index()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_x, click_y = event.pos
                    
                    #장애물 선택 취소
                    if orgin_xpos <= click_x <= orgin_xpos + 10 and orgin_ypos <= click_y <= orgin_ypos + 110:
                        selected_object.set_shape_type(VERTICAL)
                        selected_object.set_pos(orgin_x, orgin_y)
                        return NOTHING_SELECTED, None, False
                    
                    for y in range(BLOCK_NUM + OBSTACLE_NUM + 6):
                        for x in range(BLOCK_NUM + OBSTACLE_NUM):
                            if self.BOARD[y][x].contain(click_x, click_y) and isinstance(self.BOARD[y][x], ROAD):
                                if self.check_overlapping_obstacle(x, y):
                                    selected_object.set_pos(orgin_x, orgin_y)
                                    return NOTHING_SELECTED, None, False
                                
                                player_x = 0
                                player_y = 0
                                complement_player_x = 0
                                complement_player_y = 0
                                for y_pos in range(BLOCK_NUM + OBSTACLE_NUM + 6):
                                    for x_pos in range(BLOCK_NUM + OBSTACLE_NUM):
                                        if self.BOARD[y_pos][x_pos].get_state() == player:
                                            player_x = x_pos
                                            player_y = y_pos
                                        if self.BOARD[y_pos][x_pos].get_state() == self.complement(player):
                                            complement_player_x = x_pos
                                            complement_player_y = y_pos
                                            
                                if selected_object.get_shape_type() == VERTICAL:
                                    self.BOARD[index_y][index_x].set_state(FILL)
                                    self.BOARD[index_y+1][index_x].set_state(FILL)
                                    self.BOARD[index_y+2][index_x].set_state(FILL)
                                    if self.DFS(player_x, player_y, player) and self.DFS(complement_player_x, complement_player_y, self.complement(player)):
                                        selected_object.set_state(USED)
                                        selected_object.set_pos(x, y)
                                    else:
                                        self.BOARD[index_y][index_x].set_state(EMPTY)
                                        self.BOARD[index_y+1][index_x].set_state(EMPTY)
                                        self.BOARD[index_y+2][index_x].set_state(EMPTY)
                                        selected_object.set_shape_type(VERTICAL)
                                        selected_object.set_pos(orgin_x, orgin_y)
                                        return NOTHING_SELECTED, None, False
                                elif selected_object.get_shape_type() == HORIZONAL:
                                    self.BOARD[index_y][index_x].set_state(FILL)
                                    self.BOARD[index_y][index_x+1].set_state(FILL)
                                    self.BOARD[index_y][index_x+2].set_state(FILL)
                                    if self.DFS(player_x, player_y, player) and self.DFS(complement_player_x, complement_player_y, self.complement(player)):
                                        selected_object.set_state(USED)
                                        selected_object.set_pos(x, y)
                                    else:
                                        self.BOARD[index_y][index_x].set_state(EMPTY)
                                        self.BOARD[index_y][index_x+1].set_state(EMPTY)
                                        self.BOARD[index_y][index_x+2].set_state(EMPTY)
                                        selected_object.set_shape_type(VERTICAL)
                                        selected_object.set_state(UNUSED)
                                        selected_object.set_pos(orgin_x, orgin_y)
                                        return NOTHING_SELECTED, None, False
                                self.update()
                                self.print_turn(player)
                                pygame.display.flip()
                                return NOTHING_SELECTED, None, True
                                            
    def run(self):
        while True:    
            winner = self.play()
            winner_txt = None
            if winner == RED:
                winner_txt = FONT.render('RED', True, COLOR['RED'])
            elif winner == WHITE:
                winner_txt = FONT.render('WHITE', True, COLOR['WHITE'])
            game_end = FONT.render('winner:', True, COLOR['WHITE'])
            restart = FONT.render('Click to restart', True, COLOR['ASHE_BROWN'])
            self.window.blit(game_end, [CELL_SIZE*3, CELL_SIZE*15])
            self.window.blit(winner_txt, [CELL_SIZE*27, CELL_SIZE*15])
            self.window.blit(restart, [CELL_SIZE*3, CELL_SIZE*25])
            pygame.display.flip()
    
            pygame.event.clear()
    
            clicked = False
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
                    if event.type == pygame.QUIT:
                        raise
                        break


Quaridor = BOARD()

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    Quaridor.run()

pygame.quit()

