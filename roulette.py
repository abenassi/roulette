#!C:\Python27
# -*- coding: utf-8 -*-
import sys, os, time, datetime

import random
import pprint


class Roulette():
    def __init__(self):
        self.currentNumber = None
        self.histNumbers = []
        self.bet = []

    def spin(self, times=1):
        RV = []

        # spin roulette "times" times
        for i in xrange(times):
            num = random.randint(0, 36)
            self.currentNumber = num
            self.histNumbers.append(num)
            RV.append(num)

        # returns only a number (not a list) if spin 1 time
        if len(RV) == 1:
            RV = RV[0]

        return RV

    def get_history(self):
        return self.histNumbers

    def clear(self):
        self.currentNumber = None
        self.histNumbers = []


class Paper():
    def __init__(self):
        self.markedNumbers = set()
        self.numMarks = 0
        self.squareNumbers = set()

    def __repr__(self):
        string = "Marked numbers:\n\n" + str(self.markedNumbers)
        string = string + "\n\nNumber of marks: " + str(self.numMarks)
        string = string + "\n\nSquare numbers:\n\n" + str(self.squareNumbers)

        return string

    def mark(self, numbers):

        if type(numbers) == int:
            numbers = [numbers]

        for i in numbers:
            self.markedNumbers.add(i)
            self.numMarks += 1

        self.squareNumbers = self._check_squares()

    def clear(self):
        self.markedNumbers = set()
        self.numMarks = 0
        self.squareNumbers = set()

    def get_num_marks(self):
        return self.numMarks

    def get_marked_numbers(self):
        return self.markedNumbers

    def get_square_numbers(self):
        return self.squareNumbers

    def _check_squares(self):
        """Check if any unmarked number would close a square if marked."""
        RV = set()

        totalNumbers = set(xrange(0, 37))
        unmarkedNumbers = totalNumbers - self.markedNumbers

        # iterate through all unmarked numbers, looking for possible squares
        for unmarkedNumber in unmarkedNumbers:

            # create list of number sets that close a square with unmarked number
            squares = Number(unmarkedNumber).get_squares()

            # check if any potential square is all marked, but the unmarked number
            for square in squares:

                # if potential square is marked, add unmarked numbers to RV
                if square.issubset(self.markedNumbers):
                    RV.add(unmarkedNumber)

        return RV


class Number():
    def __init__(self, num):
        self.num = num

    def get_squares(self):
        RV = list()

        # list of neighbor numbers clockwise starting from left
        nbs = self.get_neighbors()

        for i in xrange(8):

            # current number
            currNgh = nbs[i]

            # next number
            if i + 1 <= 7:
                nextNgh = nbs[i + 1]
            else:
                nextNgh = nbs[i + 1 - 8]

            # next next number
            if i + 2 <= 7:
                nextNextNgh = nbs[i + 2]
            else:
                nextNextNgh = nbs[i + 2 - 8]

            # if 3 contiguous and not same row or column, they are a square
            if (currNgh and nextNgh and nextNextNgh) and \
                    self._check_diff_row([currNgh, nextNgh, nextNextNgh]) and \
                    self._check_diff_col([currNgh, nextNgh, nextNextNgh]):

                square = set([currNgh, nextNgh, nextNextNgh])

                RV.append(square)

            i += 1

        return RV

    def get_neighbors(self):
        num = self.num
        RV = list()

        # if 0, no neighbors
        if num == 0:
            RV = [None for i in xrange(8)]

        # if not 0, up to 8 neighbors are possible
        RV.append(num - 1)
        RV.append(num - 4)
        RV.append(num - 3)
        RV.append(num - 2)
        RV.append(num + 1)
        RV.append(num + 4)
        RV.append(num + 3)
        RV.append(num + 2)

        # get column of current number (from 3 columns in a cloth)
        col = self._get_col()

        # check if its in first or last row
        row = self._get_row_situation()

        # si esta en la columna izquierda o derecha tiene 3 vecinos menos
        if col == "left":
            RV[0] = None
            RV[1] = None
            RV[7] = None

        elif col == "right":
            RV[3] = None
            RV[4] = None
            RV[5] = None

        # si esta en la plrimera o ultima fila, tiene 3 vecinos menos
        if row == "first":
            RV[1] = None
            RV[2] = None
            RV[3] = None

        elif row == "last":
            RV[5] = None
            RV[6] = None
            RV[7] = None

        return RV

    def _get_col(self):
        lNumbers = []
        rNumbers = []

        # calculo los left numbers
        i = 1
        while i <= 36:
            lNumbers.append(i)
            i += 3

        # calculo los rifht numbers
        i = 3
        while i <= 36:
            rNumbers.append(i)
            i += 3

        # chequeo en que conjunto esta
        if self.num in lNumbers:
            RV = "left"
        elif self.num in rNumbers:
            RV = "right"
        else:
            RV = "middle"

        return RV

    def _get_row_situation(self):

        if self.num in [1, 2, 3]:
            RV = "first"
        elif self.num in [34, 35, 36]:
            RV = "last"
        else:
            RV = "middle"

        return RV

    def _check_diff_row(self, numbers):
        RV = True

        # ordena los numeros
        numbers.sort()

        if numbers[0] == numbers[1] - 1 and \
           numbers[1] - 1 == numbers[2] - 2:

            RV = False

        return RV

    def _check_diff_col(self, numbers):
        RV = True

        # ordena los numeros
        numbers.sort()

        if numbers[0] == numbers[1] - 3 and \
           numbers[1] - 3 == numbers[2] - 6:

            RV = False

        return RV























