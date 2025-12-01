import aoc_utils as ut
import collections
import itertools
import types
from dataclasses import dataclass

@dataclass
class Move:
    pos: int
    zeros: int

class Parser(ut.Parser):

    def __init__(self, fileName):
        super().__init__(fileName)
        self.data = list()

    def parseLine(self, y, line):
        if line.startswith("R"):
            self.data.append(int(line[1:]))
        elif line.startswith("L"):
            self.data.append(-int(line[1:]))

class Solver:

    def __init__(self, d):
        self.data = d

    def compute_positions(self, start):
        pos = []
        current = start
        for d in self.data:
            unwrapped = (current + d)
            nxt = unwrapped % 100
            if (unwrapped != nxt):
                zeros = abs(unwrapped - nxt) // 100
                if (current == 0) and (d < 0):
                    zeros -= 1
                if (nxt == 0) and (d > 0):
                    zeros -= 1
            else:
                zeros = 0

            pos.append(Move(nxt, zeros))
            current = nxt
        return pos


    def solve_part1(self):
        moves = self.compute_positions(50)
        zeros = 0
        for m in moves:
            if m.pos == 0:
                zeros += 1
        return zeros

    def solve_part2(self):
        moves = self.compute_positions(50)
        zeros = 0
        for m in moves:
            if m.pos == 0:
                zeros += 1
            if m.zeros > 0:
                zeros += m.zeros 
        return zeros