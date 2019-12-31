from spaces import Spaces

MIN_SIZE = 2
MAX_SIZE = 40

class Graph:
    def __init__(self, size=5, start=(0,0), end=(4,4)):
        self.size = size
        self.start = start
        self.end = end
        self.matrix = [[Spaces.EMPTY for j in range(size)] for i in range(size)]
        #self.matrix = np.zeros((size,size))
        self.matrix[start[0]][start[1]] = Spaces.START
        self.matrix[end[0]][end[1]] = Spaces.END
        

    def setEndPoint(self, new_point, start_or_end):
        '''
        Set the start or finish point.
        Pass Spaces.START or Spaces.END and the new point.
        
        Return 0 if space out of bounds, occupied by a barrier,
        or occupied by the opposite endpoint.

        Return 1 on success.
        '''

        if start_or_end == Spaces.START: opposite = Spaces.END
        elif start_or_end == Spaces.END: opposite = Spaces.START
        else: return 0

        if new_point[0] >= self.size or new_point[1] >= self.size: return 0
        if self.matrix[new_point[0]][new_point[1]] in [Spaces.BARRIER, opposite]: return 0
         
        old_start = self.setEndpointToEmpty(start_or_end)
        self.matrix[new_point[0]][new_point[1]] = start_or_end
        
        if start_or_end == Spaces.START: self.start = new_point
        else: self.end = new_point

        return 1
    

    def setEndpointToEmpty(self, space_type):
        '''
        Find the position of either START or END.
        Set the space to EMPTY.
        Return the position.
        '''
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == space_type:
                    self.matrix[i][j] = Spaces.EMPTY
                    return i, j

        return -1, -1 


    def toggleBarrier(self, position):
        '''
        Place or remove a barrier from a position.
        Will not work if position occupied by Spaces.START
        or Spaces.END. 

        Return 1 if a barrier was set.
        Return 0 if a barrier is turned off.
        Return -1 if a barrier could not be set or turned off
        '''
        if position[0] >= self.size or position[1] >= self.size: return -1

        if self.matrix[position[0]][position[1]] == Spaces.BARRIER:
            self.matrix[position[0]][position[1]] = Spaces.EMPTY
            return 0
        elif self.matrix[position[0]][position[1]] == Spaces.EMPTY:
            self.matrix[position[0]][position[1]] = Spaces.BARRIER
            return 1
            
        else: return -1


    def getPosition(self, x, y):
        return self.matrix[x][y]


    def resizeMatrix(self, size):
        '''
        Make matrix size x size.
        Set  Start to (0,0), Set end to (size-1,size-1).
        '''
        if size > MAX_SIZE:
            return

        self.size = size
        self.matrix = [[Spaces.EMPTY for j in range(size)] for i in range(size)]
        self.matrix[0][0] = Spaces.START
        self.matrix[size-1][size-1] = Spaces.END
        self.end = (size-1,size-1)
        self.start = (0,0)

    
    def resetMatrix(self):
        self.resizeMatrix(self.size)    