import pygame
import math
import random
import sys


class Particle():
    def __init__(self, x, y, radius,speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = 0

    def Collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.hypot(dx, dy)
        if (dist <= 10):
            return True
        else:
            return False

    def D(self, obs):
        min = sys.float_info.max
        for p in obs:
            dx = self.x - p.x
            dy = self.y - p.y
            d = math.hypot(dx, dy)
            if d < min:
                min = d
        return min

    def Collision(self):

        for p in robot:
            dx = p.x - self.x
            dy = p.y - self.y
            distance  = math.hypot(dx,dy)
            if(distance <= 10 ):
                return True
        return False
    def find_net_repulsion(self, obs,idx):
        dx = 0
        dy = 0
        neta = 1000
        for obstacle in obs:
            disx = self.x - obstacle.x
            disy = self.y - obstacle.y
            if math.hypot(disx, disy) > 30:
                magnitude = 0
            else:
                magnitude = math.hypot(disx, disy) * neta
            dx += magnitude * (self.x - obstacle.x)
            dy += magnitude * (self.y - obstacle.y)
        return (dx, dy)

    def move(self, other, obs,idx):
        prevx = self.x
        prevy = self.y
        d_star = 30
        eta = 0.01
        dx_attraction = (other.x - self.x)
        dy_attraction = (other.y - self.y)
        dist = math.hypot(dx_attraction, dy_attraction)
        if dist > d_star:
            magnitude = d_star * eta
        else:
            magnitude = eta * dist
        dx_attraction *= magnitude
        dy_attraction *= magnitude

        (dx_repulsion, dy_repulsion) = self.find_net_repulsion(obs,idx)
        dx_new=0
        dy_new=0
        magn=0
        for p in range(nor):
            if not p==idx:
                disx = self.x - robot[p].x
                disy = self.y - robot[p].y
                hyp = math.hypot(disx,disy)
                if math.hypot(disx,disy) < 25:
                    magn = hyp * 50
                    dx_new += magn * disx
                    dy_new += magn * disy
                elif hyp>200:
                    magn = 0
                elif hyp>25 and hyp<200:
                    magn = hyp  * 0.001
                    dx_new += magn * -disx
                    dy_new += magn * -disy
        dx_net = dx_repulsion  + dx_attraction + dx_new
        dy_net = dy_repulsion + dy_attraction + dy_new

        theta_attraction = (math.atan2(dy_attraction, dx_attraction))
        theta_repulsion = (math.atan2(dy_repulsion, dx_repulsion))
        theta = (math.atan2(dy_net, dx_net))

       # if math.hypot(dy_repulsion, dx_repulsion) > 0:
        #    theta = math.pi / 2 + math.atan2(dy_repulsion, dx_repulsion)
        self.x += math.cos(theta) * self.speed
        self.y += math.sin(theta) * self.speed
        while not self.Collision():
            self.x = self.x + random.randrange(1,2)
            self.y = self.y + random.randrange(1,2)

    def bounce(self):
        if self.x > width - self.radius:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = -self.angle

        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = -self.angle

        if self.y > height - self.radius:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = - self.angle

        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = - self.angle


    def moveGoal(self):
        prevx = self.x
        prevy = self.y
        if(self.y<=30 and self.x<=m-35):
            self.x = self.x + random.randrange(1,2)
        elif (self.x>=m-40 and self.y<=n-40):
            self.y = self.y + random.randrange(1,2)
        elif( self.y>=n-40 and self.x>30):
            self.x = self.x -  random.randrange(1,2)
        elif(self.x<=30 and self.y>30):
            self.y = self.y - random.randrange(1,2);

        print (self.x,self.y)
        disx = robot[0].x - self.x
        disy = robot[0].y - self.y
        min = math.hypot(disx,disy)
        for p in robot:
            disx = p.x - self.x
            disy = p.y - self.y
            dist = math.hypot(disx,disy)
            if(min > dist):
                min = dist
        if(min > 70):
            self.x = prevx
            self.y = prevy
        print (self.x,self.y,min)

    def moveObs(self):
        x = random.randrange(10,690)
        y = random.randrange(10,690)
        dx = x - self.x
        dy = y - self.y
        mag = math.hypot(dx,dy)
        dx*=mag
        dy*=mag
        theta = math.atan2(dy,dx)
        self.x+= math.cos(dx)*self.speed
        self.y+=math.sin(dy)*self.speed

pygame.init()
m = 800
n = 800
(width, height) = (m, n)
bg_color = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
run = True
goal = []
robot = []
obs = []
nor=20
clock = pygame.time.Clock()
j = random.randrange(0, 500)
k = random.randrange(0, 500)
mx = 0
for p in range(nor):
    x = random.uniform(2,70)
    y = random.uniform(2,70)
    if(mx<x):
        mx = x
    robot.append(Particle(x,y,4,2))

for p in range(20):
    x = random.uniform(10,650)
    y = random.uniform(10,650)
    s = random.uniform(0,8)
    obs.append(Particle(x,y,8,1))
goal.append(Particle(mx+20, 30, 10,0))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill(bg_color)
    for p in goal:
        p.moveGoal()
        pygame.draw.circle(screen, (255,0,255), (int(p.x), int(p.y)), p.radius)
    for p in obs:
        p.moveObs()
        p.bounce()
        pygame.draw.circle(screen, (0, 0, 0), (int(p.x), int(p.y)), p.radius)
    for i in range(nor):
        p = robot[i]
        if not p.Collide(goal[0]):
            p.move(goal[0], obs,p)
            p.bounce()
            pygame.draw.circle(screen, (0, 0, 255), (int(p.x), int(p.y)), p.radius)
        else:
            pygame.draw.circle(screen, (0, 0, 255), (int(p.x), int(p.y)), p.radius)

    pygame.display.flip()
   # clock.tick(60)
