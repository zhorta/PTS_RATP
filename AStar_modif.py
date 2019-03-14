import math
from datetime import datetime

import json

#from bson.json_util import dumps #to convert pymongo.cursor.Cursor to JSON
import pandas as pd
from pandas.io.json import json_normalize
#import geopandas as gpd
#from shapely.geometry import Point
#import matplotlib.pyplot as plt

import pymongo
from pymongo import MongoClient

import numpy as np

import gmaps
gmaps.configure(api_key='YOUR_API_KEY')

client = MongoClient()
db = client.commuteasy

class Node_:
    stop_id = 0
    coord_x = 0.0
    coord_y = 0.0
    coutTrajetEstime = 0.0
    time_to_node_g = 0
    trip_id = 0
    stop_name = ""

    def __init__(self, stop_id, neighbours, transfers, coord_x, coord_y):
        self.stop_id = stop_id
        self.neighbours = neighbours
        self.transfers = transfers
        time_to_node_g = 0
        
        self.coord_x = coord_x
        self.coord_y = coord_y
    
    def add_neighbour(self, node_to_add_id, dist):
        #self.neighbours[node_to_add.id].append(dist)
        self.neighbours.setdefault(node_to_add_id,[]).append(dist)
    def add_transfer(self, node_to_add_id, dist):
        self.transfers.setdefault(node_to_add_id,[]).append(dist)
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
    def cost_neighbours(self, current_node, next_node_id):
        cost_value = current_node.neighbours[next_node_id][0]
        return cost_value

    def cost_transfers(self, current_node, next_node_id):
        cost_value = current_node.transfers[next_node_id][0]
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
            result += self.cost_neighbours(liste_fermee[i], liste_fermee[i+1])
            i += 1
        last_value = self.cost_neighbours(liste_fermee[i], current_node)
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

print("END PART 1")

nodes = []
index = 1

for stop in stops:
    
    new_node_x = stop["stop_lon"]
    new_node_y = stop["stop_lat"]
    new_node = Node_(stop['stop_id'],{}, {}, new_node_x, new_node_y)
    new_node.stop_name = stop["stop_name"]
    
    # Adds the transfers to the transfers dict
    # --------------------------------------
    correspondances = db.transfers.find({"from_stop_id": stop['stop_id']})
    correspondances_id = []
    correspondances_duration = []
    for correspondance in correspondances:
        correspondances_id.append(correspondance["to_stop_id"])
        correspondances_duration.append(correspondance["min_transfer_time"])
    for i in range(len(correspondances_id)):
            new_node.add_transfer(correspondances_id[i], correspondances_duration[i])
    # --------------------------------------
    try:
        new_node_info = db.stop_times.find_one({"stop_id": stop['stop_id']})
        new_node_trip_id = new_node_info["trip_id"]
        new_node.trip_id = new_node_trip_id
        
        new_node_stop_sequence = new_node_info["stop_sequence"]
        
        
        voisin = db.stop_times.find_one({"trip_id": new_node_trip_id, "stop_sequence": new_node_stop_sequence + 1})
        voisin_stop_id = voisin["stop_id"]
       
    
        
        
        new_node_arrival_time = datetime.strptime(new_node_info["arrival_time"], '%H:%M:%S')
        #print(new_node_arrival_time)
        voisin_arrival_time = datetime.strptime(voisin["arrival_time"], '%H:%M:%S')
        #print(voisin_arrival_time)
        diff = (voisin_arrival_time - new_node_arrival_time).total_seconds()
        #print(diff)
        
        new_node.add_neighbour(voisin_stop_id, diff)
        
        
    except TypeError:
        pass
        #print("error with " + str(stop['stop_id']))

    
    nodes.append(new_node)

def find_node_with_id(id):
    for node in nodes:
        if node.stop_id == id:
            return node

        
def find_node_with_name(name):
    nodes_list = list()
    for node in nodes:
        if node.stop_name == name:
            nodes_list.append(node)
    return nodes_list
    
astar = A_Star()
open_list = []
closed_list = []
goal = find_node_with_id(4035022) # 1913 La Défense (4024287) # Gare de Rueil 
start = find_node_with_id(4024278) # Dunant (1713) # Gare de Rueil RER 
start.time_to_node_g = 0
open_list.append(start)

def closest_transfer_neighbour(node):
    transfers_distances = {}
    mini = ()
    for transfer in node.transfers:
        #print("test")
        #print("\t" + str(find_node_with_id(transfer).neighbours))
        Gx = node.time_to_node_g #astar.cost_G(closed_list, temp)
        #print("test2")
        for neighbour in find_node_with_id(transfer).neighbours:
            #print(find_node_with_id(transfer).neighbours[neighbour][0])
            Gy = node.time_to_node_g + node.transfers[transfer][0] + find_node_with_id(transfer).neighbours[neighbour][0]
            #print("Gy: " + str(Gy))
            k = astar.cost_transfers(node, transfer)
            #print("k: " + str(k))
            transfers_distances.setdefault(transfer,[]).append(Gy)
            mini = (min(transfers_distances, key=transfers_distances.get), transfers_distances[min(transfers_distances, key=transfers_distances.get)][0], Gx)
    return mini


while len(open_list) != 0:
    

    best = astar.best_node(open_list)
    for node in open_list:
        if node == best:
            open_list.remove(node)
    
    closed_list.append(best)

    if node.stop_id == goal.stop_id:
        break

    if astar.is_in_list(closed_list, goal.stop_id):
        open_list = []
    else:
        temp = closed_list[-1]
        
        for node in open_list:
            if not astar.is_in_list(temp.neighbours, node):
                open_list.remove(node)
        
        if len(temp.neighbours) != 0:
            for neighbour in temp.neighbours:
                min_dist_transfer_tuple = closest_transfer_neighbour(temp)

                min_dist_transfer_tuple_two = ()
            
            
            
                Gy = closed_list[-1].time_to_node_g + temp.neighbours[neighbour][0]
            
                neighbour_tuple = (neighbour, Gy)
                min_tuple = ()
                if len(min_dist_transfer_tuple) == 2:
                    min_dist_transfer_tuple_two = (min_dist_transfer_tuple[0], min_dist_transfer_tuple[1])
                    min_tuple = min(neighbour_tuple, min_dist_transfer_tuple_two)
            
                k = 0
                Gx = 0
                v = 0
                if len(min_tuple) == 2 :
                    try:
                        k = astar.cost_neighbours(temp, min_tuple[0])
                        Gx = closed_list[-1].time_to_node_g #astar.cost_G(closed_list, temp)
                        v = not astar.is_in_list(closed_list, min_tuple[0])
                    except TypeError:
                        k = astar.cost_transfers(temp, min_tuple[0])
                        Gx = min_dist_transfer_tuple[2]
                        Gy = min_tuple[1]
                        v = not astar.is_in_list(closed_list, min_tuple[0])

            
                #k = astar.cost_neighbours(temp, neighbour)
            
                if v and not astar.is_in_list(open_list, neighbour) or Gy > Gx + k :
                    g = Gx + k
                    find_node_with_id(neighbour).time_to_node_g = g
                    find_node_with_id(neighbour).coutTrajetEstime = g + astar.heuristic_value(find_node_with_id(neighbour), goal)
                    #print("g(y) = " + str(find_node_with_id(neighbour).time_to_node_g))

                    open_list.append(find_node_with_id(neighbour))

        else:
            for transfer in temp.transfers:
                min_dist_transfer_tuple = closest_transfer_neighbour(temp)
            
                k = 0
                Gx = 0
                v = 0
                
                k = astar.cost_transfers(temp, min_dist_transfer_tuple[0])
                Gx = min_dist_transfer_tuple[2]
                Gy = min_dist_transfer_tuple[1]
                v = not astar.is_in_list(closed_list, min_dist_transfer_tuple[0])

            
                #k = astar.cost_neighbours(temp, neighbour)
            
                if v and not astar.is_in_list(open_list, min_dist_transfer_tuple[0]) or Gy > Gx + k :
                    g = Gx + k
                    find_node_with_id(min_dist_transfer_tuple[0]).time_to_node_g = g
                    find_node_with_id(min_dist_transfer_tuple[0]).coutTrajetEstime = g + astar.heuristic_value(find_node_with_id(min_dist_transfer_tuple[0]), goal)
                    #print("g(y) = " + str(find_node_with_id(neighbour).time_to_node_g))

                    open_list.append(find_node_with_id(min_dist_transfer_tuple[0]))



astar.display_nodes(closed_list)

#test_input = input("From: ")
#list_test_stop_name = find_node_with_name(test_input)


stops_dictionaries_list = []

for i in range(len(closed_list)):
    dictionary = {}
    coor = (closed_list[i].coord_y, closed_list[i].coord_x)
    dictionary["coordinates"] = coor
    dictionary["name"] = db.stops.find_one({"stop_id": closed_list[i].stop_id})["stop_name"]
    dictionary["position"] = i + 1
    route = db.trips.find_one({"trip_id": closed_list[i].trip_id})
    if route is not None:
        route = route["route_id"]
        dictionary["line"] = db.routes.find_one({"route_id": route})["route_short_name"]
    else:
        dictionary["line"] = "unknown"
    stops_dictionaries_list.append(dictionary)

stops_coor = ()
for stop in stops_dictionaries_list:
    stops_coor = stops_coor + (stop["coordinates"],)


print("Route: ")
for stop in closed_list:
    name = db.stops.find_one({"stop_id": stop.stop_id})["stop_name"]
    route = db.trips.find_one({"trip_id": stop.trip_id})
    if route is not None:
        route = route["route_id"]
        line = db.routes.find_one({"route_id": route})["route_short_name"]
        print("line : " + str(line))
    print("id : " + str(stop.stop_id))
    print("name : " + name)
        
print("END")    
    

stops_locations = [stop['coordinates'] for stop in stops_dictionaries_list]
info_box_template = """
<dl>
<dt>Name</dt><dd>{name}</dd>
<dt>Line</dt><dd>{line}</dd>
<dt>Stop number </dt><dd>{position}</dd>
</dl>
"""
stops_info = [info_box_template.format(**stop) for stop in stops_dictionaries_list]
marker_layer = gmaps.marker_layer(stops_locations, info_box_content=stops_info)
fig = gmaps.figure()
fig.add_layer(marker_layer)

#final_route = gmaps.directions_layer(stops_coor)

#for i in range(len(stops_coor)-1):
#    fig.add_layer(gmaps.directions_layer(stops_coor[i], stops_coor[i+1]))


#fig.add_layer(final_route)
fig



#print(final_route_df.head())
#print("total time: ")
#print(str(closed_list[-1].time_to_node_g/60) + "min")
# print("Route: ")
# for stop in closed_list:
#    name = db.stops.find_one({"stop_id": stop.stop_id})["stop_name"]
#    route = db.trips.find_one({"trip_id": stop.trip_id})
#    if route is not None:
#        route = route["route_id"]
#        line = db.routes.find_one({"route_id": route})["route_short_name"]
#        print("line : " + str(line))
#    print("id : " + str(stop.stop_id))
#    print("name : " + name)
       
# print("END")

# new_node_route = db.trips.find_one({"trip_id": new_node_trip_id})["route_id"]
#         new_node_line = db.routes.find_one({"route_id": new_node_route})["route_short_name"]
#         new_node.line = new_node_line
