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
            if p==self:
                continue;
            dx = p.x - self.x
            dy = p.y - self.y
            distance = math.hypot(dx, dy)
            if (distance <= 10):
                return True
        for p in rgrp:
            if p==self:
                continue;
            dx = p.x - self.x
            dy = p.y - self.y
            distance = math.hypot(dx, dy)
            if (distance <= 50):
                return True
        return False

    def find_net_repulsion(self):
        dx = 0
        dy = 0
        neta = 0.005
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

    def move(self, other,idx):
        d_star = 30
        eta = 1000
        dx_attraction = (other.x - self.x)
        dy_attraction = (other.y - self.y)
        dist = math.hypot(dx_attraction, dy_attraction)
        if dist > d_star:
            magnitude = d_star * eta
        else:
            magnitude = eta/10 * dist
        dx_attraction *= magnitude
        dy_attraction *= magnitude

        (dx_repulsion, dy_repulsion) = self.find_net_repulsion()
        dx_new=0
        dy_new=0
        magn=0
        for p in range(nor):
            disx = self.x - robot[p].x
            disy = self.y - robot[p].y
            hyp = math.hypot(disx,disy)
            print (idx,hyp,"blue")
            if hyp < 25 and hyp!=0:
                magn =  hyp * 100000
                if (idx == 2):
                    magn = magn * 2
                dx_new += magn * disx
                dy_new += magn * disy
                print ("repl")
            elif hyp > 200 and idx==1:
                magn = 0
            elif idx==1 and hyp>25 and hyp<200:
                magn = hyp  * 10
                dx_new += magn * (-disx)
                dy_new += magn * (-disy)
                print (magn * (-disx),"kfk")

        dx_req = dy_req = 0
        for p in range(nor):
            disx = self.x - rgrp[p].x
            disy = self.y - rgrp[p].y
            hyp = math.hypot(disx,disy)
            print (idx,hyp)
            if hyp<25 and hyp!=0:
                magn = hyp * 100000
                if(idx==1):
                    magn = magn*2
                dx_req += magn * disx
                dy_req += magn * disy
            elif hyp > 200 and idx==2:
                magn = 0
            elif hyp<200 and hyp>25 and idx==2:
                magn = hyp * 10
                dx_req += magn * -disx
                dy_req += magn * -disy

        dx_net = dx_repulsion  + dx_attraction + dx_new + dx_req
        dy_net = dy_repulsion + dy_attraction + dy_new + dy_req

        theta = (math.atan2(dy_net, dx_net))

        if math.hypot(dy_repulsion, dx_repulsion) > 0 :
            theta = math.pi / 2 + math.atan2(dy_repulsion, dx_repulsion)
        self.x += math.cos(theta) * self.speed
        self.y += math.sin(theta) * self.speed
        #while self.Collision():
            #self.x = self.x + random.randrange(0,1)
            #self.y = self.y + random.randrange(0,1)

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
        if(self.y<=30 and self.x<=665):
            self.x = self.x + random.randrange(2,4)
        elif (self.x>=660 and self.y<=660):
            self.y = self.y + random.randrange(2,4)
        elif( self.y>=660 and self.x>30):
            self.x = self.x -  random.randrange(2,4)
        elif(self.x<=30 and self.y>30):
            self.y = self.y - random.randrange(2,4);

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
(width, height) = (700, 700)
bg_color = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
run = True
goal = []
robot = []
obs = []
rgrp = []
nor = 15
clock = pygame.time.Clock()
j = random.randrange(0, 500)
k = random.randrange(0, 500)
goal.append(Particle(680, 680, 10,0))
goal.append(Particle(20, 20, 10,0))

for p in range(nor):
    x = random.uniform(2,200)
    y = random.uniform(2,200)
    robot.append(Particle(x,y,4,3))

for p in range(nor):
    x = random.uniform(420,695)
    y = random.uniform(420,695)
    rgrp.append(Particle(x,y,4,3))

for p in range(50):
    x = random.uniform(10,650)
    y = random.uniform(10,650)
    obs.append(Particle(650,20,8,0))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill(bg_color)

    for p in goal:
        pygame.draw.circle(screen, (255,255,0), (int(p.x), int(p.y)), p.radius)
    for p in obs:
        pygame.draw.circle(screen, (0, 0, 0), (int(p.x), int(p.y)), p.radius)

    for i in range(nor):
        p = robot[i]
        if not p.Collide(goal[0]):
            p.move(goal[0],1)
            p.bounce()
            pygame.draw.circle(screen, (0, 0, 255), (int(p.x), int(p.y)), p.radius)
        else:
            pygame.draw.circle(screen, (0, 0, 255), (int(p.x), int(p.y)), p.radius)

    for i in range(nor):
        p = rgrp[i]
        if not p.Collide(goal[1]):
            p.move(goal[1],2)
            p.bounce()
            pygame.draw.circle(screen, (255, 0, 0), (int(p.x), int(p.y)), p.radius)
        else:
            pygame.draw.circle(screen, (255, 0, 0), (int(p.x), int(p.y)), p.radius)

    pygame.display.flip()
    clock.tick(60)
