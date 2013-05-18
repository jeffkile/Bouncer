import time
class JeffsMinPriorityQueue(object):
    def __init__(self):
        self.pq = [0] #store values starting at index 1
        self.N = 0 #number of items in queue
    def isEmpty(self):
        return self.N == 0
    def insert(self,key):
        self.N += 1
        self.pq.append(key)
        self.swim(self.N)
    def delMin(self):
        if(self.isEmpty()): raise Exception("The Priority Queue is Empty") 
        #print "array, n", self.pq, self.N
        self.exch(1, self.N)
        min = self.pq[self.N]
        self.N -= 1
        self.sink(1)
        del self.pq[self.N+1] #Im not sure if del's arrange resizing algo is efficent enough, may need to replace this
        return min 
    def swim(self, k):
        while k>1 and self.greater(k/2, k):
            self.exch(k, k/2)
            k = k/2
    def sink(self,k):
        while 2*k <= self.N:
            j = 2*k #children of node k are 2k and 2k+1
            if j<self.N and self.greater(j, j+1):
                j += 1
            if not(self.greater(k,j)):
                break
            self.exch(k,j)
            k = j
    def greater(self,i, j):
        return self.pq[i] > self.pq[j]
    def exch(self, i, j):
        tmp = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = tmp
    def isMinHeap(self,k):
        if(k > self.N): return True
        left = 2 * k
        right = left + 1
        if(left <= self.N and self.greater(k, left)): return False
        if(right <= self.N and self.greater(k, right)): return False
        return self.isMinHeap(left) and self.isMinHeap(right)
