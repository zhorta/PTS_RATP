using System;
using System.Collections.Generic;
namespace Commuteasy
{
    public class Node
    {
        public int id;
        public Dictionary<int, int> neighbours;
        public Node predecessor;

        public Node(int id)
        {
            this.id = id;
            this.neighbours = new Dictionary<int, int>();

        }

        public void AddNeighbour(Node node, int dist){
            neighbours.Add(node.id, dist);
        }
    }
}
