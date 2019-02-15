import math
from datetime import datetime


import pymongo
from pymongo import MongoClient

import numpy as np

client = MongoClient()
db = client.commuteasy

class Node:

    id = 0
    coord_x = 0.0
    coord_y = 0.0
    adjacent_nodes = []
    neighbours = {}
    heuristique = 0.0
    coutdudepartG = 0.0
    coutTrajetEstime = 0.0

    def __init__(self, value1, coord1, coord2, listeNodes):
        self.id = value1
        self.coord_x = coord1
        self.coord_y = coord2
        self.adjacent_nodes = listeNodes

    def __str__(self):
        return "node: {}".format(self.id)

class Node_:
    stop_id = 0
    dist_to_node = 0
    coord_x = 0.0
    coord_y = 0.0
    coutTrajetEstime = 0.0
    time_to_node_g = 0

    def __init__(self, stop_id, neighbours, coord_x, coord_y):
        self.stop_id = stop_id
        self.neighbours = neighbours
        dist_to_node = 0.0
        self.coord_x = coord_x
        self.coord_y = coord_y
    
    def add_neighbour(self, node_to_add_id, dist):
        #self.neighbours[node_to_add.id].append(dist)
        self.neighbours.setdefault(node_to_add_id,[]).append(dist)
class A_Star:

    # Heuristique: calcul de la distance entre le noeud courant et l'objectif
    #------------------------------------------------------------------------
    def heuristic_value(self, current_node, goal_node):
        x1 = current_node.coord_x
        y1 = current_node.coord_y
        x2 = goal_node.coord_x
        y2 = goal_node.coord_y
        heuristic = math.trunc(math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2)))

        return heuristic
    
    # Coût entre deux noeuds
    # -------------------------------------------------------------------------
    # def cost(self, adjacency_matrix, current_node, next_node):
    #     indL = current_node.id
    #     indC = next_node.id
    #     return adjacency_matrix[indL - 1][indC - 1]
    
    def cost(self, current_node, next_node):
        cost_value = current_node.neighbours[next_node.stop_id][0]
        return cost_value

    def display_nodes(self, nodes_list):
        result = ""
        for node in nodes_list:
            result += str(node.stop_id) + " "
    
    def build_adj_matrix(self, nodes_list):
        matrix = np.zeros((len(nodes_list), len(nodes_list)))
        
        #First, the matrix is filled with "infinite values"
        for i in range(len(nodes_list)):
            for j in range(len(nodes_list)):
                matrix[i,j] = math.inf

        for node in nodes_list:
            for key, value in node.neighbours.items():
                
                matrix[node.id, key] = node.neighbours[key][0]
        
        return matrix



    def matrix3(self):
        matrix = np.zeros((9,9))
        l0 = [0, 1, 3, 6, 0, 0, 0, 0, 0]
        l1 = [0, 0, 2, 0, 0, 0, 0, 0, 0]
        l2 = [0, 0, 0, 0, 0, 2, 0, 0, 0]
        l3 = [0, 0, 0, 0, 6, 0, 0, 0, 0]
        l4 = [0, 0, 4, 0, 0, 0, 1, 3, 1]
        l5 = [0, 0, 0, 0, 0, 0, 7, 0, 0]
        l6 = [0, 0, 0, 0, 0, 0, 0, 4, 0]
        l7 = [0, 0, 0, 0, 0, 0, 0, 0, 2]
        l8 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        matrix[0] = l0
        matrix[1] = l1
        matrix[2] = l2
        matrix[3] = l3
        matrix[4] = l4
        matrix[5] = l5
        matrix[6] = l6
        matrix[7] = l7
        matrix[8] = l8
        return matrix

    # Calcul du coût du trajet du départ au noeud courant
    #-------------------------------------------------------------------------
    # def cost_G(self, adjacency_matrix, liste_fermee, current_node):
    #     result = 0.0
    #     i = 0
    #     while i < len(liste_fermee) - 1:
    #         result += self.cost(adjacency_matrix, liste_fermee[i], liste_fermee[i+1])
    #         i += 1
    #     result += self.cost(adjacency_matrix, liste_fermee[i], current_node)
    #     return result

    def cost_G(self, liste_fermee, current_node):
        result = 0.0
        i = 0
        while i < len(liste_fermee) - 1:
            result += self.cost(liste_fermee[i], liste_fermee[i+1])
            i += 1
        last_value = self.cost(liste_fermee[i], current_node)
        result += last_value
        return result
    
    # fonction qui trouve le noeud ayant le meilleur f (trajet estimé min)
    #-------------------------------------------------------------------------
    def best_node(self, nodes_list):
        min_dist = nodes_list[0].coutTrajetEstime
        result = nodes_list[0]
        for i in range(len(nodes_list)):
            if min_dist > nodes_list[i].coutTrajetEstime:
                min_dist = nodes_list[i].coutTrajetEstime
                result = nodes_list[i]
            
        return result
    
    # Fonction qui vérifie que node est bien dans la liste
    def is_in_list(self, nodes_list, node):
        result = False
        for item in nodes_list:
            if item.stop_id == node.stop_id:
                result = True
            
        return result


# node9 = Node(9, 6, -1, [])
# node8 = Node(8, 7, 1, [node9])
# node7 = Node(7, 6, 4, [node8])
# node6 = Node(6, 4, 5, [node7] )
# node3 = Node(3, 2, 3.5,[node6] )
# node5 = Node(5, 2, 0, [node3, node7, node8, node9])
# node4 = Node(4, 0, 2, [node5] )
# node2 = Node(2, 2, 7, [node3] )
# node1 = Node(1, 0, 5, [node2, node3, node4])

# astar = A_Star()
# matrix = astar.matrix3()
# open_list = []
# closed_list = []
# goal = node9
# open_list.append(node1)

# while len(open_list) != 0:
#     best = astar.best_node(open_list)
#     for node in open_list:
#         if node == best:
#             open_list.remove(node)
    
#     closed_list.append(best)

#     if astar.is_in_list(closed_list, goal):
#         open_list = []
#     else:
#         temp = closed_list[-1]

#         for node in open_list:
#             if not astar.is_in_list(temp.adjacent_nodes, node):
#                 open_list.remove(node)
        
#         for i in range(len(temp.adjacent_nodes)):
#             Gx = astar.cost_G(matrix, closed_list, temp)
#             Gy = astar.cost_G(matrix, closed_list, temp.adjacent_nodes[i])
#             k = astar.cost(matrix, temp, temp.adjacent_nodes[i])
#             v = not astar.is_in_list(closed_list, temp.adjacent_nodes[i])
#             if v and not astar.is_in_list(open_list, temp.adjacent_nodes[i]) or Gy > Gx + k :
#                 g = Gx + k
#                 temp.adjacent_nodes[i].coutdudepartG = g
#                 temp.adjacent_nodes[i].coutTrajetEstime = g + astar.heuristic_value(temp.adjacent_nodes[i], goal)
#                 print("g(y) = " + str(temp.adjacent_nodes[i].coutdudepartG))

#                 open_list.append(temp.adjacent_nodes[i])


# astar.display_nodes(closed_list)
# print(closed_list[-1].coutdudepartG)

# node0 = Node_(0,1234,{})
# node1 = Node_(1, 3245, {})
# node2 = Node_(2, 3245, {})
# node3 = Node_(3, 3245, {})
# node4 = Node_(4, 3245, {})
# node5 = Node_(5, 3245, {})
# node6 = Node_(6, 3245, {})
# node0.add_neighbour(node1, 1)
# node0.add_neighbour(node2, 2)
# node0.add_neighbour(node3, 3)
# node0.add_neighbour(node4, 7)
# node1.add_neighbour(node0, 1)
# node1.add_neighbour(node2, 4)
# node2.add_neighbour(node0, 2)
# node2.add_neighbour(node1, 4)
# node2.add_neighbour(node6, 2)
# node3.add_neighbour(node0, 3)
# node4.add_neighbour(node0, 7)
# node4.add_neighbour(node6, 4)
# node4.add_neighbour(node5, 1)
# node5.add_neighbour(node4, 1)
# node6.add_neighbour(node2, 2)
# node6.add_neighbour(node4, 4)

# nodes = [node0, node1, node2, node3, node4, node5, node6]

# astart = A_Star()
# adj_matrix = astart.build_adj_matrix(nodes)
# print(adj_matrix)

stops = db.stops.find()
nb_of_stops = db.stops.count()

routes = db.routes.find()


# I created indexes because the search part was sooooooo long
db.stop_times.create_index([("stop_id", pymongo.ASCENDING)])
db.stop_times.create_index([("trip_id", pymongo.ASCENDING)])
db.stop_times.create_index([("stop_sequence", pymongo.ASCENDING)])
db.stop_times.create_index([("arrival_time", pymongo.ASCENDING)])
#db.stops.create_index([("stop_id", pymongo.ASCENDING)])

nodes = []
index = 1
for stop in stops:
    
    new_node_x = stop["stop_lon"]
    new_node_y = stop["stop_lat"]
    new_node = Node_(stop['stop_id'],{}, new_node_x, new_node_y)
    try:
        new_node_info = db.stop_times.find_one({"stop_id": stop['stop_id']})
        new_node_trip_id = new_node_info["trip_id"]
        new_node_stop_sequence = new_node_info["stop_sequence"]
        
        voisin = db.stop_times.find_one({"trip_id": new_node_trip_id, "stop_sequence": new_node_stop_sequence + 1})
        voisin_stop_id = voisin["stop_id"]
        
        # new_node_arrival_time = datetime.strptime(new_node_info["arrival_time"], '%H:%M:%S')
        # print(new_node_arrival_time)
        # voisin_arrival_time = datetime.strptime(voisin["arrival_time"], '%H:%M:%S')
        # print(voisin_arrival_time)
        # diff = voisin_arrival_time - new_node_arrival_time
        # print(diff)
        
        new_node.add_neighbour(voisin_stop_id, 1)# diff)
        
    except TypeError:
        pass
        #print("error with " + str(stop['stop_id']))

    
    nodes.append(new_node)

# for node in nodes:
#     print("node: ")
#     print(node.stop_id)
#     print(node.neighbours)
#     print(node.coord_x)
#     print(node.coord_y)
    

def find_node_with_id(id):
    for node in nodes:
        if node.stop_id == id:
            return node

    
astar = A_Star()
open_list = []
closed_list = []
goal = find_node_with_id(4024287)
open_list.append(find_node_with_id(4024227))


while len(open_list) != 0:
    best = astar.best_node(open_list)
    for node in open_list:
        if node == best:
            open_list.remove(node)
    
    closed_list.append(best)

    if astar.is_in_list(closed_list, goal):
        open_list = []
    else:
        temp = closed_list[-1]

        for node in open_list:
            if not astar.is_in_list(temp.neighbours, node):
                open_list.remove(node)
        
        for neighbour in temp.neighbours:
            Gy = astar.cost_G(closed_list, find_node_with_id(neighbour))
            Gx = astar.cost_G(closed_list, temp)
            k = astar.cost(temp, neighbour)
            v = not astar.is_in_list(closed_list, neighbour)
            if v and not astar.is_in_list(open_list, neighbour) or Gy > Gx + k :
                g = Gx + k
                neighbour.coutdudepartG = g
                neighbour.coutTrajetEstime = g + astar.heuristic_value(neighbour, goal)
                print("g(y) = " + str(neighbour.coutdudepartG))

                open_list.append(neighbour)


astar.display_nodes(closed_list)
print(closed_list[-1].coutdudepartG)

