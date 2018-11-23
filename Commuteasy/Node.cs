using System;
using System.Collections.Generic;
namespace Commuteasy
{
    public class Node
    {
        public int id;
        public Dictionary<int, int> neighbours;
        public Node predecessor;
        public int distToNode;

        public Node(int id)
        {
            this.id = id;
            neighbours = new Dictionary<int, int>();
            distToNode = 0;

        }

        public void AddNeighbour(Node node, int dist){
            neighbours.Add(node.id, dist);
        }
    }
}
