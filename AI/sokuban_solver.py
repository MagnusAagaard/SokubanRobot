#!/usr/bin/env python3

import os
import numpy as np
import itertools
import time

class Node:
    def __init__(self, parent, hash_val, move):
        self.parent = parent
        self.hash = hash_val
        self.hCost = 0
        self.calc_h_cost()
        if self.parent != None:
            self.gCost = parent.gCost + 1
            self.move = move
        else:
            self.gCost = 0
        self.fCost = self.hCost + self.gCost

    def calc_h_cost(self):
        self.hCost = 0

    def get_cans(self):
        cans_hash = self.hash[4:]
        cans = list()
        for i in range(0,len(cans_hash),4):
            cans.append((int(cans_hash[i:i+2]), int(cans_hash[i+2:i+4])))
        return cans

    def get_robot(self):
        robot_hash = self.hash[:4]
        return (int(robot_hash[0:2]), int(robot_hash[2:4]))


class SokubanSolver:
    def __init__(self, map_file_path):
        self.map = []
        self.can_positions = []
        self.goal_positions = list()
        self.robot_position = 0
        self._setup(map_file_path)
        self.closed_list = {}
        self.open_list = {}
        solution = self.breath_first()
        if solution == -1:
            print("Could not find solution!")
        else:
            print(solution)
        #self.find_goals()

    def _setup(self, map_file_path):
        with open(map_file_path) as f:
            l = f.read()
            row = 0
            col = 0
            row_chars = []
            for char in l:
                if char == '\n':
                    self.map.append(row_chars)
                    row_chars = []
                    row += 1
                    col = 0
                else:
                    if char == 'J':
                        self.can_positions.append((row, col))
                    elif char == 'G':
                        self.goal_positions.append((row,col))
                    elif char == 'M':
                        self.robot_position = (row,col)
                    row_chars.append(char)
                    col += 1
        #self.goal_positions = np.asarray(self.goal_positions)
        #self.can_positions = np.asarray(self.can_positions)
        print("Map loaded:")
        for r in self.map:
            print(r)

    def find_goals(self):
        costs = []
        cost = []

        for i in range(len(self.can_positions)):
            can_cost = []
            for j in range(len(self.goal_positions)):
                can_cost.append(abs(self.can_positions[i][0] - self.goal_positions[j][0]) + abs(self.can_positions[i][1] - self.goal_positions[j][1]))
            costs.append(can_cost)

        index = [i for i in range(len(self.can_positions))]
        perm = itertools.permutations(index)
        index = []
        for i in perm:
            index.append(i)
        for i in index:
            print(costs[i[0]])
            cost.append(costs[0][i[0]] + costs[1][i[1]] + costs[2][i[2]] + costs[3][i[3]])
        print(cost)

    def breath_first(self):
        root_hash = self.create_hash(self.can_positions, self.robot_position)
        root = Node(None, root_hash, None)
        self.open_list[root_hash] = root
        count = 0

        while len(self.open_list):
            count += 1
            current_node_hash = next(iter(self.open_list))
            current_node = self.open_list.pop(current_node_hash)
            if count % 100000 == 0:
                self.trace_solution(current_node)
            if self.check_solved(current_node):
                sol = self.trace_solution(current_node)
                return sol
            self.closed_list[current_node_hash] = current_node
            rob = current_node.get_robot()
            moves = [(1,0),(-1,0),(0,1),(0,-1)]
            for move in moves:
                cans = current_node.get_cans()
                rob_new = [rob[0] + move[0], rob[1] + move[1]]
                child = Node(current_node, self.create_hash(cans, rob_new), move)
                legal_move = self.check_legal_move(child, move)
                if legal_move:
                    child_hash = child.hash
                    if self.closed_list.get(child_hash) == None:
                        self.open_list[child_hash] = child
            
        print(count)
        return -1
                    

    def check_legal_move(self, child, move):
        map_array = self.map
        child_robot = child.get_robot()
        char = map_array[child_robot[0]][child_robot[1]]
        if char == 'X':
            return False
        child_cans = child.get_cans()
        for i in range(len(child_cans)):
            if child_robot == child_cans[i]:
                can_new = (child_robot[0] + move[0], child_robot[1] + move[1])
                for j in range(len(child_cans)):
                    if can_new == child_cans[j]:
                        return False
                char = map_array[can_new[0]][can_new[1]]
                if char == 'X':
                    return False
                child_cans[i] = can_new
                child_hash = self.create_hash(child_cans, child_robot)
                child.hash = child_hash
                return True
        return True


    def check_solved(self, node):
        cans = node.get_cans()
        goals = self.goal_positions
        number_of_goals = 0
        for can in cans:
            for goal in goals:
                if can == goal:
                    number_of_goals += 1

        if number_of_goals == len(goals):
            return True
        else:
            return False

    def trace_solution(self, node):
        moves = []
        translated_moves = ""
        current_node = node
        while current_node.parent != None:
            moves.append(current_node.move)
            current_node = current_node.parent

        moves.reverse()
        for move in moves:
            if move == (-1,0):
                translated_moves += 'u'
            elif move == (1,0):
                translated_moves += 'd'
            elif move == (0,1):
                translated_moves += 'r'
            elif move== (0,-1):
                translated_moves += 'l'

        print(len(translated_moves))

        return translated_moves


    def create_hash(self, cans, robot):
        #robot_postion (0x,0y), cans ((0x1,0y1), (0x2,0y2)...) 
        hash_val = ""
        if robot[0] < 10:
            hash_val += "0" + str(robot[0])
        else:
            hash_val += str(robot[0])
        if robot[1] < 10:
            hash_val += "0" + str(robot[1])
        else:
            hash_val += str(robot[1])
        for can in cans:
            if can[0] < 10:
                hash_val += "0" + str(can[0])
            else:
                hash_val += str(can[0])
            if can[1] < 10:
                hash_val += "0" + str(can[1])
            else:
                hash_val += str(can[1])
        return hash_val

        


    

if __name__ == "__main__":
    #Problemer? Check hård og blød paranteser ;)
    map_file_path = "./AI/map.txt"
    tic = time.perf_counter()
    solver = SokubanSolver(map_file_path)
    toc = time.perf_counter()
    print(f"Solved in {toc - tic:0.4f} seconds")