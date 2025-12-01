import aoc_utils as ut
import collections
import itertools
import types

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
            current = (current + d) % 100
            pos.append(current)
        return pos


    def solve_part1(self):
        imm_pos = self.compute_positions(50)
        zeros = 0
        for pos in imm_pos:
            if pos == 0:
                zeros += 1
        return zeros

    def solve_part2(self):
        pass