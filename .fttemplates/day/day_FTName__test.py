import unittest
from day<FTName> import *
import aoc_utils as ut

class TestDay<FTName>(unittest.TestCase):

    def test_parse(self):
        d = Parser.ex(0)

    def _test_solve_part1_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 0)

    def _test_solve_part1(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 0)

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