import jeffsminpriorityqueue 
import particle 
import event
from Tkinter import *
import time
import numpy as np
#import multiprocessing 

class CollisionSystem(object):
    def __init__(self):
        self.t = 0 #simulation clock time
        self.hz = 4.0 #number of redraw events per clock tick
        self.particles = [particle.Particle() for i in range(50)]
        self.pq = jeffsminpriorityqueue.JeffsMinPriorityQueue()
        self.windowWidth = 600 
        self.windowHeight = 480

        #initalize drawing stuff
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight)
        self.canvas.pack()

        self.root.after(1000, self.simulate, 10000)
        self.root.mainloop()
    
    #initalize the priority queue with all the new events for a particle a
    def predict(self, a, limit):
        if(a == None): return False 
  
        #particle particle collisions
        for p in self.particles:
            dt = a.time_to_hit(p)
            if(self.t + dt <= limit):
                e = event.Event(self.t + dt, a, p)
                self.pq.insert(e)

        #particle wall collisions
        dtX = a.time_to_hit_vertical_wall()
        dtY = a.time_to_hit_horizontal_wall()
        if((self.t + dtX) <= limit): self.pq.insert(event.Event(self.t + dtX, a, None))
        if((self.t + dtY) <= limit): self.pq.insert(event.Event(self.t + dtY, None, a))
        
    def redraw(self, limit):
        self.canvas.delete("all")
        for p in self.particles:
            params = p.draw()
            self.canvas.create_oval(params[0]*self.windowWidth, params[1]*self.windowHeight, params[2]*self.windowWidth, params[3]*self.windowHeight, fill=params[4])

        self.canvas.update() 

        if self.t < limit:
            self.pq.insert(event.Event(self.t + 1.0 / self.hz, None, None))
        
#        time.sleep(1)
    def simulate(self, limit):
        #initiate pq with collision events and redraw events
        for p in self.particles:
            self.predict(p, limit)
        self.pq.insert(event.Event(0, None, None)) #redraw event

        while self.pq.isEmpty() == False:
            e = self.pq.delMin() 
            if not (e.is_valid()): continue 
            a = e.a
            b = e.b

            #physical collision so update positions and then simulation clock
            for p in self.particles:
                p.move(e.time - self.t)
 
            self.t = e.time
            
            if a is not None and b is not None: a.bounce_off(b)
            elif a is not None and b is None: a.bounce_off_vertical_wall()
            elif a is None and b is not None: b.bounce_off_horizontal_wall()
            elif a is None and b is None: self.redraw(limit)

            #update the priority queue with the new collisions involving a or b
            self.predict(a, limit)
            self.predict(b, limit)

