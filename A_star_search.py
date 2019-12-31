from collections import namedtuple
import heapq
from spaces import Spaces

Node = namedtuple("Node", "f g position parent")
TERMINATE = Node(-1,-1,(-1,-1), None)

def CityBlockHeuristic(here, there):
    return abs(here[0] - there[0]) + abs(here[1] - there[1])


def EuclideanHeuristic(here, there):
    return (here[0] - there[0]) * (here[0] - there[0]) + \
        (here[1] - there[1]) * (here[1] - there[1])


class AStarSearch:
    
    def __init__(self, heuristic=CityBlockHeuristic):
        self.graph = None
        self.heuristic = heuristic
        self.frontier = []
        self.explored_set = []


    def setHeuristic(self, h):
        self.heuristic = h


    def setGraph(self, graphMatrix):
        self.graph = graphMatrix

    
    def startSearch(self, start, end):
        
        g = 0
        h = self.heuristic(start, end)
        n = Node(g + h, g, start, None)

        heapq.heappush(self.frontier, n)

    def iterateSearch(self, end):
        '''
        Perform a step in the search. 
        Return 1 if position if end is found.
        Else return 0 and continue the search.
        '''
        q = heapq.heappop(self.frontier)
        
        # End the search
        if q.position == end:
            return q
        
        for p in self.getNeighbors(q):
        
            if p[0] < len(self.graph) and p[0] >= 0 and p[1] < len(self.graph) and p[1] >= 0:
                if self.graph[p[0]][p[1]] != Spaces.BARRIER:
                    h = self.heuristic(p, end)
                    g = q.g + 1
                    successor = Node(g + h, g, p, q)

                # Make sure there isn't a better path to the current position already in the pipe
                # and that there isn't already a better known way to get there
                    if not self.isBetterNodeInFrontier(successor) and not self.isBetterNodeInExploredSet(successor):
                        heapq.heappush(self.frontier, successor)
            
        
        self.explored_set.append(q)

        # No path
        if len(self.frontier) == 0:
            return TERMINATE
        
        # Continue the search
        return None
        
    
    def getNeighbors(self, n):
        '''
        Return the adjacent spaces to Node n
        '''
        p = n.position
        return [(p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1)]


    def isBetterNodeInFrontier(self, n):
        '''
        Check if the node is already present in the frontier
        with a better f value. 
        Return 1 if a better node instance exists.
        Return 0 otherwise.
        '''
        for s in self.frontier:
            if n.position == s.position and s.f <= n.f:
                return 1
        
        return 0
    

    def isBetterNodeInExploredSet(self, n):
        '''
        Same as checking frontier
        '''
        for s in self.explored_set:
            if n.position == s.position and s.f <= n.f:
                return 1
        return 0


    def clearSearch(self):
        '''
        Reset all of the search data structures.
        Needs to be called after each run of the search
        '''
        self.explored_set.clear()
        self.frontier.clear()
        self.graph = None


    def search(self, start, end):

        self.startSearch(start, end)

        n = None

        while n == None:
            n = self.iterateSearch(end)

        if n == TERMINATE:
            print("No path from start to end\n")
        else:
            self.printPath(n)
    
    def printPath(self, n):
        
        while n != None:
            self.graph[n.position[0]][n.position[1]] = 'P'
            n = n.parent
        
        for l in self.graph:
            print(l)
    

