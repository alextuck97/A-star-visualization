from graph import *
import unittest

class TestGraphMethods(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def tearDown(self):
        pass

    def testSetEndpointToEmpty(self):
        self.assertEqual(self.g.getPosition(0,0),Spaces.START)
        self.assertEqual(self.g.getPosition(4,4), Spaces.END)

        old_start = self.g.setEndpointToEmpty(Spaces.START)
        self.assertEqual(old_start, (0,0))
        self.assertEqual(self.g.getPosition(0,0), Spaces.EMPTY)
    

    def testSetEndPoint(self):
        # Set start on end and end on start. Expecting failure.
        success = self.g.setEndPoint((4,4), Spaces.START)
        self.assertEqual(success, 0)
        success = self.g.setEndPoint((0,0), Spaces.END)
        self.assertEqual(success, 0)

        # Set out of bounds
        success = self.g.setEndPoint((self.g.size, self.g.size), Spaces.END)
        self.assertEqual(success, 0)

        # Set legally
        new_start = (1,2)
        success = self.g.setEndPoint(new_start, Spaces.START)
        self.assertEqual(success,1)
        self.assertEqual(new_start,self.g.start)

        new_end = (3,3)
        success = self.g.setEndPoint(new_end, Spaces.END)
        self.assertEqual(success,1)
        self.assertEqual(new_end,self.g.end)


    def testResize(self):
        self.g.resizeMatrix(MAX_SIZE + 1)
        self.assertNotEqual(self.g.size, MAX_SIZE + 1)
        
        self.g.resizeMatrix(10)
        self.assertEqual(self.g.size, 10)
        self.assertEqual(self.g.end, (9,9))

    
    def testToggleBarrier(self):
        # Set barrier on start. 
        success = self.g.toggleBarrier((0,0))
        self.assertEqual(success, -1)

        # Set barrier on end
        success = self.g.toggleBarrier((4,4))
        self.assertEqual(success,-1)

        # Set barrier out of bounds
        success = self.g.toggleBarrier((100,100))
        self.assertEqual(success,-1)

        # Set barrier in legal position
        success = self.g.toggleBarrier((3,3))
        self.assertEqual(success,1)
        self.assertEqual(self.g.getPosition(3,3), Spaces.BARRIER)

        # Unset barrier
        success = self.g.toggleBarrier((3,3))
        self.assertEqual(success,0)
        self.assertEqual(self.g.getPosition(3,3), Spaces.EMPTY)
