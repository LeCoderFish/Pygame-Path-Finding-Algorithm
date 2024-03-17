import pygame as pg 
import math
import time
import heapq

size=[1000,1000]
rows=20
columns=20

class Screen():
    def __init__(self):
        pg.init()
        self.screen=pg.display.set_mode((size[0],size[1]))
        data=[[0 for _ in range(columns)] for _ in range(rows)]
        open_set=[]
        w=[1]
        list1=[]
        a=[1]

        grid=Grid(self.screen,rows,columns,data)
        running=True
        while running==True:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    running=False
                grid.build(event)
            self.screen.fill((255,255,255)) 
            if grid.start and grid.end:
                initialize(data,list1,grid.start,grid.end,open_set,w)
                astar(data,list1,open_set,a)
                time.sleep(0.01)
            grid.draw()     
            pg.display.update()  
            
class Grid():
    def __init__(self,screen,rows,columns,data):
        self.screen=screen
        self.data=data
        self.rows=rows
        self.columns=columns
        self.start=0
        self.end=0
    def build(self,event):
        mouse_buttons=pg.mouse.get_pressed()
        if mouse_buttons[0]:
            if event.pos[0]<1000 and event.pos[0]>0 and event.pos[1]<1000 and event.pos[1]>0:
                self.data[math.floor(event.pos[0]/(size[0]/self.rows))][math.floor(event.pos[1]/(size[1]/self.columns))]=1
        elif mouse_buttons[2]:
            if self.start==0:
                if event.pos[0]<1000 and event.pos[0]>0 and event.pos[1]<1000 and event.pos[1]>0:
                    self.data[math.floor(event.pos[0]/(size[0]/self.rows))][math.floor(event.pos[1]/(size[1]/self.columns))]='start'
                    self.start=[math.floor(event.pos[0]/(size[0]/self.rows)),math.floor(event.pos[1]/(size[1]/self.columns))]
            elif self.end==0:
                if event.pos[0]<1000 and event.pos[0]>0 and event.pos[1]<1000 and event.pos[1]>0:
                    self.data[math.floor(event.pos[0]/(size[0]/self.rows))][math.floor(event.pos[1]/(size[1]/self.columns))]='end'
                    self.end=[math.floor(event.pos[0]/(size[0]/self.rows)),math.floor(event.pos[1]/(size[1]/self.columns))]
    def draw(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.data[i][j]==1:
                    pg.draw.rect(self.screen, (0,0,0), (i*(size[0]/self.rows),j*(size[0]/self.rows),(size[0]/self.rows-2),(size[0]/self.rows-2)))
                if self.data[i][j]=='start':
                    pg.draw.rect(self.screen, (0,0,255), (i*(size[0]/self.rows),j*(size[0]/self.rows),(size[0]/self.rows-2),(size[0]/self.rows-2)))
                if self.data[i][j]=='end':
                    pg.draw.rect(self.screen, (255,0,0), (i*(size[0]/self.rows),j*(size[0]/self.rows),(size[0]/self.rows-2),(size[0]/self.rows-2)))
                if self.data[i][j]=='passed':
                    pg.draw.rect(self.screen, (0,255,0), (i*(size[0]/self.rows),j*(size[0]/self.rows),(size[0]/self.rows-2),(size[0]/self.rows-2)))
                if self.data[i][j]=='path':
                    pg.draw.rect(self.screen, (255,0,255), (i*(size[0]/self.rows),j*(size[0]/self.rows),(size[0]/self.rows-2),(size[0]/self.rows-2)))
                    
class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value  # The value of the node in the matrix
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Estimated cost from current node to target node
        self.f = 0  # Total cost: f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal):
    # Using Manhattan distance as a heuristic
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def initialize(matrix,list1,start,goal,open_set,w):
    if w[0]==1:
        list1.append(Node(start[0],start[1], matrix[start[0]][start[1]]))
        list1.append(Node(goal[0],goal[1], matrix[goal[0]][goal[1]]) )
        open_set.append(list1[0])
        heapq.heapify(open_set)   
        list1.append(set())
        w[0]=0

def astar(matrix,list1,open_set,a):
    if a[0]==1:
        current = heapq.heappop(open_set)
        if current.x == list1[1].x and current.y == list1[1].y:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            a[0]=0
            for element in path:
                matrix[element[0]][element[1]]='path'
            return None

        list1[2].add(current)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = current.x + dx, current.y + dy

            if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y]!= 1 and matrix[x][y]!='start' and matrix[x][y]!='passed':
                neighbor = Node(x, y, matrix[x][y])
                matrix[x][y]='passed'
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor, list1[1])
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

                if neighbor in list1[2]:
                    continue

                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)

        return None

               
        
Screen()