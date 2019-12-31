import unittest
from graph import *
from A_star_search import *
import numpy as np

class testAStarMethods(unittest.TestCase):
    
    def setUp(self):
        self.graph = Graph()
        self.a_star = AStarSearch()
    

    def test_cityblockheuristic(self):
        a = CityBlockHeuristic((1,1),(2,2))
        self.assertEqual(a,2)

        a = CityBlockHeuristic((0,0),(1,0))
        self.assertEqual(a,1)
    

    def test_euclideanheuristic(self):
        a = EuclideanHeuristic((1,1),(2,2))
        self.assertAlmostEqual(a,2)

        a = EuclideanHeuristic((1,1), (4,2))
        self.assertAlmostEqual(a, 10)
