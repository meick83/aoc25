import aoc_utils as ut
import collections
import itertools
import types

class Parser(ut.Parser):

    def __init__(self, fileName):
        super().__init__(fileName)
        self.data = ut.Grid()

    def _parse_cell(self, x, y, ch):
        self.data[ut.Point(x,y)] = (ch == '@')


class Solver:

    def __init__(self, d):
        self.data = d

    def count_adjacent(self):
        r = ut.Grid(self.data.width, self.data.height)
        for p in self.data.points():
            used = 0
            for dx, dy in itertools.product((-1,0,1), repeat=2):
                if (dx == 0) and (dy == 0):
                    continue
                q = p.translate_x(dx).translate_y(dy)
                if not self.data.is_inside(q):
                    continue
                if self.data[q]:
                    used += 1
            r[p] = used
        return r



    def solve_part1(self):
        ag = self.count_adjacent()
        r = 0
        for p in ag.points():
            if self.data[p] and ag[p] < 4:
                r += 1
        return r

    def solve_part2(self):
        pass