using System;
using System.Collections.Generic;
using System.Linq;

namespace Commuteasy
{
    public class Dijkstra
    {
        Graph graph;
        //List<Node> path;

        public Dijkstra(Graph graph)
        {
            this.graph = graph;
            //path = new List<Node>();
        }

        /*public int[] FromVisited(List<int> visited){ //Function that finds the shortest path from a visited node to an unvisited node
            int minDist = int.MaxValue;
            int selectedVertex = -1;
            int destinationVertex = -1;
            int[] toReturn = new int[3];

            if(visited.Count>0){
                
                foreach (int vertex in visited)
                {
                    for (int j = 0; j < graph.adjacencyMatrix.GetLength(0); j++)
                    {
                        if (!visited.Contains(j) && graph.adjacencyMatrix[vertex, j] < minDist)
                        {
                            minDist = graph.adjacencyMatrix[vertex, j];
                            destinationVertex = j;
                            selectedVertex = vertex;
                        }
                    }

                }
            }

            toReturn[0] = minDist;
            toReturn[1] = selectedVertex;
            toReturn[2] = destinationVertex;



            return toReturn;
        }*/

        public object[] FromVisited(List<Node> visited)
        { //Function that finds the shortest path from a visited node to an unvisited node
            int minDist = int.MaxValue;
            Node selectedVertex = new Node(-1);
            Node destinationVertex = new Node(-1);
            object[] toReturn = new object[3];
            List<int> visitedIds = new List<int>();

            foreach(Node vertexId in visited){
                //Console.WriteLine(vertexId.id);
                visitedIds.Add(vertexId.id);
            }


            if (visited.Count > 0)
            {

                foreach (Node vertex in visited)
                {
                    for (int j = 0; j < graph.adjacencyMatrix.GetLength(0); j++)
                    {
                        if (!visitedIds.Contains(j) && graph.adjacencyMatrix[vertex.id, j] != int.MaxValue && graph.adjacencyMatrix[vertex.id, j] + vertex.distToNode < minDist)
                        {
                            minDist = graph.adjacencyMatrix[vertex.id, j] + vertex.distToNode ;
                            destinationVertex = graph.nodes[j];
                            selectedVertex = vertex;
                            destinationVertex.distToNode = minDist;// + selectedVertex.distToNode;
                            //Console.WriteLine("Dist To Node " + destinationVertex.id + " = " + destinationVertex.distToNode);
                        }
                    }

                }
            }

            toReturn[0] = minDist;
            toReturn[1] = selectedVertex;
            toReturn[2] = destinationVertex;



            return toReturn;
        }

        public List<Node> ShortestPath(Node start, Node end)
        {
            List<Node> path = new List<Node>();
            List<Node> visited = new List<Node>();

            bool reachedTheEnd = false;

            int minDist = int.MaxValue;
            int distToNode = 0;

            Node currentVertex = start;
            Node nextVertex = new Node(-1);

            while (!reachedTheEnd)
            {
                
                visited.Add(currentVertex);

                object[] distFromVisited = FromVisited(visited); //index 0 = minDist, index 1 = selectedVertex, index 2 = destinationVertex

                if ((int)distFromVisited[0] < minDist)
                {
                    minDist = (int)distFromVisited[0];
                    nextVertex = (Node)distFromVisited[2];
                    currentVertex = (Node)distFromVisited[1];
                }


                Console.WriteLine("Visited: ");
                foreach (Node vertex in visited)
                {
                    Console.Write(vertex.id + ", ");
                }
                Console.WriteLine();


                Console.Write("Current vertex: " + currentVertex.id);

                //path.Add(currentVertex);
                nextVertex.predecessor = currentVertex;
                currentVertex = nextVertex;


                Console.WriteLine(" — Next vertex: " + currentVertex.id);
                Console.WriteLine("Distance to next vertex: " + currentVertex.distToNode);
                minDist = int.MaxValue;

                Console.WriteLine();
                Console.WriteLine();
                Console.WriteLine();

                if (currentVertex.id == end.id)
                {
                    reachedTheEnd = true;
                    path.Add(currentVertex);
                    Console.WriteLine("Total distance to reach " + end.id + " from " + start.id + ": " + currentVertex.distToNode);
                }

                
            }
            Node test = currentVertex;

            while(test.predecessor != null){
                path.Add(test.predecessor);
                test = test.predecessor;
            }

            return path;
        }
    }
}
