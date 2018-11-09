using System;
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
            node1.AddNeighbour(node2, 1);
            node2.AddNeighbour(node0, 2);
            node2.AddNeighbour(node1, 1);
            node3.AddNeighbour(node0, 3);

            List<Node> nodes = new List<Node>();
            nodes.Add(node0);
            nodes.Add(node1);
            nodes.Add(node2);
            nodes.Add(node3);

            Graph graph = new Graph(nodes);
            graph.PrintAdjMatrix();
        }
    }
}
