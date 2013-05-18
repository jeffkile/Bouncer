#An event that occurs during a poarticle collision simulation
#Each event contains the time at which the event will occur (assuming no interupting action) and particle a and b involved
# - a and b are both null: redraw event
# - a nul,l b not null: collision with vertical wall
# - a not, null b null: collision with horizontal wall
# - a and b not null: binary collision between a and b

class Event(object):
    def __init__(self, t, aParticle, bParticle): 
        #time that event is scheduled to occur:
        self.time = t
        #particles involved in collision:
        self.a = aParticle 
        self.b = bParticle
        #collision counts at event creation:
        self.countA = aParticle.count if aParticle is not None else -1
        self.countB = bParticle.count if bParticle is not None else -1

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def is_valid(self):
        if(self.a is not None and self.a.count != self.countA):
            return False
        if(self.b is not None and self.b.count != self.countB):
            return False
        return True
