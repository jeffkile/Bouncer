import numpy as np

class Particle(object):
    def __init__(self):
        self.rx, self.ry = np.random.randint(100)/100.0, np.random.randint(100)/100.0 #position
        self.vx = self.vy = 0.02
        if(np.random.randint(2) == 1):
            self.vx = -self.vx
        if(np.random.randint(2) == 1):
            self.vy = -self.vy
        self.r = 0.01
        self.mass = 0.5 
        self.count = 0 #number of collisions
        self.color = 'black'
        self.dx = 0
        self.dy = 0

    def move(self, dt):
        self.dx = self.vx * dt
        self.dy = self.vy * dt

        self.rx += self.dx 
        self.ry += self.dy 

    def draw(self):
        return (self.rx-self.r, self.ry-self.r, self.rx+self.r, self.ry+self.r, self.color)

    def time_to_hit(self, b):
        a = self
        if(a == b): return float('inf')
        dx = b.rx - a.rx
        dy = b.ry - a.ry
        dvx = b.vx - a.vx
        dvy = b.vy - a.vy
        dvdr = dx * dvx + dy * dvy
        if(dvdr > 0): return float('inf')
        dvdv = dvx * dvx + dvy * dvy
        drdr = dx * dx + dy * dy
        sigma = a.r + b.r
        d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma)
        if(d < 0): return float('inf')
        return -(dvdr + np.sqrt(d)) / dvdv

    def time_to_hit_vertical_wall(self):
        if (self.vx > 0): return ((1.0 - self.rx - self.r) / self.vx)
        elif (self.vx < 0): return ((self.r - self.rx) / self.vx)
        else: return float('inf') 

    def time_to_hit_horizontal_wall(self):
        if (self.vy > 0): return ((1.0 - self.ry - self.r) / self.vy)
        elif (self.vy < 0): return ((self.r - self.ry) / self.vy)
        else: return float('inf')
        
    def bounce_off(self, that):
        dx = that.rx - self.rx
        dy = that.ry - self.ry
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy #dv dot dr
        dist = that.r + self.r #distance between particle centers at collision

        #normal force F and its values in x and y directions
        force = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)
        fx = force * dx / dist
        fy = force * dy / dist
       
        #update velocities according to normal foce
        self.vx += fx / self.mass #f/m = a, , so this is adding acceleration to the velocity variable ...maybe future implement acceleration and friction
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        #update collision count
        self.count += 1
        that.count += 1

    def bounce_off_vertical_wall(self):
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_wall(self):
        self.vy = -self.vy
        self.count += 1

    def kinetic_energy(self):
        return 0.5 * mass * (self.vx * self.vx + self.vy * self.vy)
