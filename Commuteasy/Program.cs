﻿using System;
using System.Collections.Generic;

namespace Commuteasy
{
    class Program
    {
        static void Main(string[] args)
        {
            Node node0 = new Node(0);
            Node node1 = new Node(1);
            Node node2 = new Node(2);
            Node node3 = new Node(3);
            node0.AddNeighbour(node1, 1);
            node0.AddNeighbour(node2, 2);
            node0.AddNeighbour(node3, 3);
            node1.AddNeighbour(node0, 1);
            node1.AddNeighbour(node2, 4);
            node2.AddNeighbour(node0, 2);
            node2.AddNeighbour(node1, 4);
            node3.AddNeighbour(node0, 3);

            List<Node> nodes = new List<Node>
            {
                node0,
                node1,
                node2,
                node3
            };

            Graph graph = new Graph(nodes);
            graph.PrintAdjMatrix();

            Dijkstra graphDijkstra = new Dijkstra(graph);
            List<int> visited = new List<int> { 3, 0, 1 };
            Console.WriteLine("Dist: " + graphDijkstra.FromVisited(visited)[0]);
            Console.WriteLine("From: " + graphDijkstra.FromVisited(visited)[1]);
            Console.WriteLine("To: " + graphDijkstra.FromVisited(visited)[2]);
            List<int> graphPath = graphDijkstra.ShortestPath(3, 2);
            Console.WriteLine("Path");
            foreach(int vertex in graphPath){
                Console.WriteLine(vertex);
            }
        }
    }
}
