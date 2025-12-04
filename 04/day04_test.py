import unittest
from day04 import *
import aoc_utils as ut

class TestDay04(unittest.TestCase):

    def test_parse(self):
        d = Parser.ex(0)
        self.assertFalse(d[0,0])
        self.assertTrue(d[1,1])

    def test_count_adjacent(self):
        d = Parser.ex(0)
        s = Solver(d)
        ag = s.count_adjacent()
        self.assertEqual(ag[0,0], 2)
        self.assertEqual(ag[1,1], 6) 

    def test_solve_part1_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 13)

    def test_solve_part1(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 1435)

    def _test_solve_part2_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part2(), 0)

    def _test_solve_part2(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part2(), 0)

if __name__ == '__main__':
    unittest.main()