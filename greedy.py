from collections import defaultdict
import os
os.system("python qubo.py")

def edge_coloring(edges, num_colors):
    # Create a dictionary to store the final color of each edge
    edge_colors = {}

    # Create a dictionary to store the colors of adjacent edges
    adjacent_colors = defaultdict(set)

    # Iterate through the edges and color them one by one
    for u, v in edges:
        # Find the set of available colors for the current edge
        available_colors = set(range(1, num_colors + 1))
        available_colors -= adjacent_colors[u]
        available_colors -= adjacent_colors[v]

        # Assign the smallest available color to the current edge
        color = min(available_colors)
        edge_colors[(u, v)] = color

        # Update the colors of adjacent edges
        adjacent_colors[u].add(color)
        adjacent_colors[v].add(color)

    return edge_colors


print(edge_coloring(edge_list, colors))