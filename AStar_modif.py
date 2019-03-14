import math
from datetime import datetime


import pymongo
from pymongo import MongoClient

import numpy as np

<<<<<<< HEAD
import gmaps
gmaps.configure(api_key='YOUR_API_KEY')

=======
>>>>>>> parent of c0b0fc5... Update AStar_modif.py
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
    coord_x = 0.0
    coord_y = 0.0
    coutTrajetEstime = 0.0
    time_to_node_g = 0
    trip_id = 0
    stop_name = ""

    def __init__(self, stop_id, neighbours, coord_x, coord_y):
        self.stop_id = stop_id
        self.neighbours = neighbours
        time_to_node_g = 0
        
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
    def cost(self, current_node, next_node_id):
        cost_value = current_node.neighbours[next_node_id][0]
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

    # Calcul du coût du trajet du départ au noeud courant
    #-------------------------------------------------------------------------
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
    def is_in_list(self, nodes_list, find_node_id):
        result = False
        
        for item in nodes_list:
            if type(item) == int :
                if item == find_node_id:
                    result = True
            if type(item) == Node_:
                if item.stop_id == find_node_id:
                    result = True
            
        return result

stops = db.stops.find()
nb_of_stops = db.stops.count()

routes = db.routes.find()


# I created indexes because the search part was sooooooo long
db.stop_times.create_index([("stop_id", pymongo.ASCENDING)])
db.stop_times.create_index([("trip_id", pymongo.ASCENDING)])
db.stop_times.create_index([("stop_sequence", pymongo.ASCENDING)])
db.stop_times.create_index([("arrival_time", pymongo.ASCENDING)])
db.transfers.create_index([("from_stop_id", pymongo.ASCENDING)])
db.routes.create_index([("route_short_name", pymongo.ASCENDING)])
db.stops.create_index([("stop_name", pymongo.ASCENDING)])

nodes = []
index = 1
for stop in stops:
    
    new_node_x = stop["stop_lon"]
    new_node_y = stop["stop_lat"]
    new_node = Node_(stop['stop_id'],{}, new_node_x, new_node_y)
    new_node.stop_name = stop["stop_name"]
    
    # Adds the changes to the neighbours
    # --------------------------------------
    # correspondances = db.transfers.find({"from_stop_id": stop['stop_id']})
    # correspondances_id = []
    # correspondances_duration = []
    # for correspondance in correspondances:
    #     correspondances_id.append(correspondance["to_stop_id"])
    #     correspondances_duration.append(correspondance["min_transfer_time"])
    # for i in range(len(correspondances_id)):
    #         new_node.add_neighbour(correspondances_id[i], correspondances_duration[i])
    try:
        new_node_info = db.stop_times.find_one({"stop_id": stop['stop_id']})
        new_node_trip_id = new_node_info["trip_id"]
        new_node.trip_id = new_node_trip_id
        
        new_node_stop_sequence = new_node_info["stop_sequence"]
        
        
        voisin = db.stop_times.find_one({"trip_id": new_node_trip_id, "stop_sequence": new_node_stop_sequence + 1})
        voisin_stop_id = voisin["stop_id"]
       
    
        
        
        # new_node_arrival_time = datetime.strptime(new_node_info["arrival_time"], '%H:%M:%S')
        # print(new_node_arrival_time)
        # voisin_arrival_time = datetime.strptime(voisin["arrival_time"], '%H:%M:%S')
        # print(voisin_arrival_time)
        # diff = voisin_arrival_time - new_node_arrival_time
        # print(diff)
        
        new_node.add_neighbour(voisin_stop_id, 60)# diff) 60 sec
        
        
    except TypeError:
        pass
        #print("error with " + str(stop['stop_id']))

    
    nodes.append(new_node)

def find_node_with_id(id):
    for node in nodes:
        if node.stop_id == id:
            return node

    
astar = A_Star()
open_list = []
closed_list = []
goal = find_node_with_id(1913) # La Défense (4024287) # Gare de Rueil 
start = find_node_with_id(1713) # Gare de Rueil RER (4024278) # Dunant
start.time_to_node_g = 0
open_list.append(start)



while len(open_list) != 0:
    
    best = astar.best_node(open_list)
    for node in open_list:
        if node == best:
            open_list.remove(node)
    
    closed_list.append(best)

    if astar.is_in_list(closed_list, goal.stop_id):
        open_list = []
    else:
        temp = closed_list[-1]
        
        for node in open_list:
            if not astar.is_in_list(temp.neighbours, node):
                open_list.remove(node)
        
        for neighbour in temp.neighbours:
            Gx = closed_list[-1].time_to_node_g #astar.cost_G(closed_list, temp)
            Gy = closed_list[-1].time_to_node_g + temp.neighbours[neighbour][0]
            k = astar.cost(temp, neighbour)
            v = not astar.is_in_list(closed_list, neighbour)
            if v and not astar.is_in_list(open_list, neighbour) or Gy > Gx + k :
                g = Gx + k
                find_node_with_id(neighbour).time_to_node_g = g
                find_node_with_id(neighbour).coutTrajetEstime = g + astar.heuristic_value(find_node_with_id(neighbour), goal)
                print("g(y) = " + str(find_node_with_id(neighbour).time_to_node_g))

                open_list.append(find_node_with_id(neighbour))
    


astar.display_nodes(closed_list)
print(closed_list[-1].time_to_node_g)
print("Route: ")
for stop in closed_list:
    name = db.stops.find_one({"stop_id": stop.stop_id})["stop_name"]
    route = db.trips.find_one({"trip_id": stop.trip_id})["route_id"]
    line = db.routes.find_one({"route_id": route})["route_short_name"]
    print("id : " + str(stop.stop_id))
    print("name : " + name)
    print("line : " + str(line))
print("END")

# new_node_route = db.trips.find_one({"trip_id": new_node_trip_id})["route_id"]
#         new_node_line = db.routes.find_one({"route_id": new_node_route})["route_short_name"]
#         new_node.line = new_node_line

