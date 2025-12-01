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
        moves = s.compute_positions(50)
        self.assertEqual(moves[0].pos, 82)
        self.assertEqual(moves[0].zeros, 1)
        self.assertEqual(moves[1].pos, 52)
        self.assertEqual(moves[1].zeros, 0)

    def test_compute_positions_r1000(self):
        d = [1000]
        s = Solver(d)
        moves = s.compute_positions(50)
        self.assertEqual(moves[0].pos, 50)
        self.assertEqual(moves[0].zeros, 10)

    def test_compute_positions_l1000(self):
        d = [-1000]
        s = Solver(d)
        moves = s.compute_positions(50)
        self.assertEqual(moves[0].pos, 50)
        self.assertEqual(moves[0].zeros, 10)

    def test_compute_positions_l101(self):
        d = [-101]
        s = Solver(d)
        moves = s.compute_positions(1)
        self.assertEqual(moves[0].pos, 0)
        self.assertEqual(moves[0].zeros, 1)

    def test_solve_part1_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 3)

    def test_solve_part1(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part1(), 1055)

    def test_solve_part2_ex(self):
        d = Parser.ex(0)
        s = Solver(d)
        self.assertEqual(s.solve_part2(), 6)

    def test_solve_part2(self):
        d = Parser.input()
        s = Solver(d)
        self.assertEqual(s.solve_part2(), 6386)

if __name__ == '__main__':
    unittest.main()
