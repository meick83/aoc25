import unittest
from day01 import *
import aoc_utils as ut

class TestDay01(unittest.TestCase):

    def test_parse(self):
        d = Parser.ex(0)
        self.assertEqual(d[0], -68)
        self.assertEqual(d[2],  48)

    def test_compute_positions(self):
        d = Parser.ex(0)
        s = Solver(d)
        imm_pos = s.compute_positions(50)
        self.assertEqual(imm_pos[0], 82)
        self.assertEqual(imm_pos[1], 52)

    def test_solve_part1_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 3)

    def test_solve_part1(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 1055)

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
