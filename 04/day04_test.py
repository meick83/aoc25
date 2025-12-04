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
        self.assertIsNone(ag[0,0])
        self.assertEqual(ag[1,1], 6) 

    def test_solve_part1_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 13)

    def test_solve_part1(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 1435)

    def test_remove_rolls(self):
        d = Parser.ex(0)
        s = Solver(d)
        ag0 = s.count_adjacent()
        rr0 = s.removable_rolls(ag0)
        ag1 = s.remove_rolls(ag0, rr0)
        rr1 = s.removable_rolls(ag1)
        self.assertEqual(len(rr1), 12)
        ag2 = s.remove_rolls(ag1, rr1)
        rr2 = s.removable_rolls(ag2)
        self.assertEqual(len(rr2), 7)
        ag3 = s.remove_rolls(ag2, rr2)
        rr3 = s.removable_rolls(ag3)
        self.assertEqual(len(rr3), 5)

    def test_solve_part2_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part2(), 43)

    def test_solve_part2(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part2(), 8623)

if __name__ == '__main__':
    unittest.main()