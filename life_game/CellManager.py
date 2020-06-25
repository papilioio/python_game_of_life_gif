#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import os
import random

from .Const import Const

class CellManager:
    update_count = 0
    def __init__(self,cols,rows, steps, threshold):
        self.cols = cols
        self.rows = rows
        self.steps = steps
        self.threshold = threshold
        self.cell_list = []
        self.history = []

    def create_cells(self,randomize=False):
        for x, y in itertools.product(range(self.cols), range(self.rows)):
            cell = {
                    'x': x,
                    'y': y,
                    'status' : Const.STATUS_DIE,
                    'status_next' : ''
                }
            if randomize is True:
                cell.update({
                    'status' : Const.STATUS_ALIVE if random.random() > self.threshold else Const.STATUS_DIE
                })
            self.cell_list.append(cell)
        self.set_next_status()

    def run(self):
        new_hist = []
        for t in range(self.steps):
            self.update_count += 1
            self.update_status()
            self.set_next_status()
            new_hist.append({'step' : [c.copy() for c in self.cell_list]})
        self.history = new_hist

    def get_update_count(self):
        return self.update_count

    def set_next_status(self):
        for c in self.cell_list:
            naighbor_cells = self.get_neighbor_cells(c.get('x'), c.get('y'))
            # alive_count = self.get_neighbor_alive_count(c.get('x'), c.get('y'))
            alive_count = len([n for n in naighbor_cells if n['status'] is Const.STATUS_ALIVE])
            if c['status'] is Const.STATUS_DIE and alive_count is 3:
                c['status_next'] = Const.STATUS_ALIVE
            else:
                c['status_next'] = Const.STATUS_DIE

            if c['status'] is Const.STATUS_ALIVE:
                if alive_count is 2 or alive_count is 3:
                    c['status_next'] = Const.STATUS_ALIVE
                else:
                    c['status_next'] = Const.STATUS_DIE
        

    def update_status(self):
        for c in self.cell_list:
            c['status'] = c['status_next']

    def get_neighbor_alive_count(self, x_offset, y_offset):
        alive_count = 0
        for x, y in itertools.product(range(-1, 2), repeat=2):
            try:
                if x is 0 and y is 0:
                    continue
                naighbor = [c for c in self.cell_list if c.get('x') is x + x_offset and c.get('y') is y + y_offset][0]
                # print(naighbor)
                if naighbor['status'] is Const.STATUS_ALIVE:
                    alive_count += 1
            except IndexError: continue
            
        return alive_count

    def get_neighbor_cells(self,x_offset, y_offset):
        naighbor_list = []
        for x, y in itertools.product(range(-1, 2), repeat=2):
            try:
                if x==0 and y == 0:
                    continue
                naighbor = [
                    c for c in self.cell_list if c['x'] is x+x_offset and c['y'] is y+y_offset
                ][0]
                naighbor_list.append(naighbor)
            except IndexError: continue
        return naighbor_list
