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

        public int[] FromVisited(List<int> visited){ //Function that finds the shortest path from a visited node to an unvisited node
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
        }

        public List<int> ShortestPath(int start, int end){
            List<int> path = new List<int>();
            List<int> visited = new List<int>();

            bool reachedTheEnd = false;

            int minDist = int.MaxValue;
            int totalDist = 0;

            int currentVertex = start;
            int nextVertex = -1;

            while(!reachedTheEnd){
                
                visited.Add(currentVertex);
                int[] distFromVisited = FromVisited(visited); //index 0 = minDist, index 1 = selectedVertex, index 2 = destinationVertex

                if(distFromVisited[0]<minDist){
                    minDist = distFromVisited[0];
                    nextVertex = distFromVisited[2];
                    currentVertex = distFromVisited[1];
                }


                Console.WriteLine("Visited: ");
                foreach(int vertex in visited){
                    Console.Write(vertex + ", ");
                }
                Console.WriteLine();


                Console.Write("Current vertex: " + currentVertex);

                totalDist += minDist;
                path.Add(currentVertex);
                currentVertex = nextVertex;

                Console.WriteLine(" — Next vertex: " + currentVertex);
                minDist = int.MaxValue;

                if(currentVertex == end){
                    reachedTheEnd = true;
                    path.Add(currentVertex);
                } 
            }


            return path;
        }
    }
}
