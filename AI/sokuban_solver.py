#!/usr/bin/env python3

import os
import numpy as np
import itertools

class Node:
    def __init__(self, parent, cans, robot, hash_val, move):
        self.parent = parent
        self.hash = hash_val
        self.cans = cans
        self.robot = robot
        self.hCost = 0
        self.calc_h_cost()
        if self.parent != None:
            self.gCost = parent.gCost + 1
            self.moves = list(parent.moves)
            self.moves.append(move)
        else:
            self.gCost = 0
            self.moves = []
        self.fCost = self.hCost + self.gCost

    def calc_h_cost(self):
        self.hCost = 0


class SokubanSolver:
    def __init__(self, map_file_path):
        self.map = []
        self.can_positions = []
        self.goal_positions = []
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
                        self.can_positions.append([row, col])
                    elif char == 'G':
                        self.goal_positions.append([row,col])
                    elif char == 'M':
                        self.robot_position = [row,col]
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
        root = Node(None, self.can_positions, self.robot_position, root_hash, None)
        self.open_list[root_hash] = root
        count = 0

        while len(self.open_list):
            count += 1
            current_node_hash = next(iter(self.open_list))
            current_node = self.open_list.pop(current_node_hash)
            self.closed_list[current_node_hash] = current_node

            rob = list(current_node.robot)
            moves = [(1,0),(-1,0),(0,1),(0,-1)]
            for move in moves:
                cans = list(current_node.cans)
                rob_new = [rob[0] + move[0], rob[1] + move[1]]
                child = Node(current_node, cans, rob_new, self.create_hash(cans, rob_new), move)
                legal_move = self.check_legal_move(child, move)
                if legal_move:
                    child_hash = self.create_hash(child.cans, rob_new)
                    if self.closed_list.get(child_hash) == None:
                        self.open_list[child_hash] = child
            
            self.trace_solution(current_node)
            if self.check_solved(current_node):
                sol = self.trace_solution(current_node)
                return sol

        print(count)
        return -1
                    

    def check_legal_move(self, child, move):
        map_array = self.map
        char = map_array[child.robot[0]][child.robot[1]]
        if char == 'X':
            return False
        for i in range(len(child.cans)):
            if child.robot == child.cans[i]:
                can_new = [child.robot[0] + move[0], child.robot[1] + move[1]]
                for j in range(len(child.cans)):
                    if can_new == child.cans[j]:
                        return False
                char = map_array[can_new[0]][can_new[1]]
                if char == 'X':
                    return False
                child.cans[i] = can_new
        return True


    def check_solved(self, node):
        cans = node.cans
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
        sol = []
        translated_moves = ""
        current_node = node
        while current_node.parent != None:
            sol.append(current_node.robot)
            current_node = current_node.parent

        sol.reverse()
        for move in node.moves:
            if move == (-1,0):
                translated_moves += 'u'
            elif move == (1,0):
                translated_moves += 'd'
            elif move == (0,1):
                translated_moves += 'r'
            elif move== (0,-1):
                translated_moves += 'l'

        print(len(translated_moves))

        return sol


    def create_hash(self, cans, robot):
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
    map_file_path = "./AI/map.txt"
    solver = SokubanSolver(map_file_path)