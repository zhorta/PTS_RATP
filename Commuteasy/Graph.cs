using System;
using System.Collections.Generic;

namespace Commuteasy
{
    public class Graph
    {
        public List<Node> nodes;
        public int[,] adjacencyMatrix;

        public int [,] BuildAdjMatrix(List<Node> nodes){
            int[,] matrix = new int [nodes.Count, nodes.Count];

            //First, the matrix is filled with "infinite values"
            for (int i = 0; i < nodes.Count; i++){
                for (int j = 0; j < nodes.Count; j++){
                    matrix[i, j] = int.MaxValue;
                }
            }

            foreach(Node node in nodes){
                foreach(int key in node.neighbours.Keys){
                    matrix[node.id, key] = node.neighbours[key];
                    //Console.WriteLine(node.neighbours[key]);
                }
            }

            return matrix;
        }

        public int GetNbOfNodes(){
            return nodes.Count;
        }

        public Graph(List<Node> nodes)
        {
            this.nodes = nodes;
            this.adjacencyMatrix = BuildAdjMatrix(nodes);

        }

        public void PrintAdjMatrix(){
            for (int i = 0; i < adjacencyMatrix.GetLength(0); i++){
                for (int j = 0; j < adjacencyMatrix.GetLength(1); j++){
                    if(adjacencyMatrix[i,j] == int.MaxValue){
                        Console.Write("+∞" + " ");
                    }
                    else{
                        Console.Write(adjacencyMatrix[i, j] + " ");
                    }

                }
                Console.WriteLine();
            }
        }
    }
}
