import operator
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


node = Node(parent=None,hash_val="0",move=(1,2))
node1 = Node(parent=None,hash_val="1",move=(1,2))
node2 = Node(parent=None,hash_val="2",move=(1,2))
node.fCost = 5
node1.fCost = 10
node2.fCost = 3
open_list = {}
open_list["0"] = node
open_list["1"] = node1
open_list["2"] = node2
print(open_list.keys())
print(min(open_list.values(), key=operator.attrgetter('fCost')))
#node_test = open_list.pop(min_key)
#print(node_test.fCost)
#node3 = Node(parent=None,hash_val="3",move=(1,2))
#node3.fCost = 7