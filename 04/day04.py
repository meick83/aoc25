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
            if not self.data[p]:
                r[p] = None
                continue
            for q in self.adjacent_points(p):
                if self.data[q]:
                    used += 1
            r[p] = used
        return r

    def adjacent_points(self, p):
        r = []
        for dx, dy in itertools.product((-1,0,1), repeat=2):
            if (dx == 0) and (dy == 0):
                continue
            q = p.translate_x(dx).translate_y(dy)
            if not self.data.is_inside(q):
                continue
            r.append(q)
        return r

    def removable_rolls(self, ag):
        r = set()
        for p in ag.points():
            adj = ag[p]
            if adj is not None and adj < 4:
                r.add(p)
        return r

    def remove_rolls(self, ag, rr):
        res = ag.copy()
        for p in rr:
            res[p] = None
            for q in self.adjacent_points(p):
                if res[q] is None:
                    continue
                res[q] -= 1
        return res

    def solve_part1(self):
        ag = self.count_adjacent()
        return len(self.removable_rolls(ag))

    def solve_part2(self):
        ag = self.count_adjacent()
        rr = self.removable_rolls(ag)
        score = 0
        while len(rr) > 0:
            score += len(rr)
            ag = self.remove_rolls(ag, rr)
            rr = self.removable_rolls(ag)
        return score