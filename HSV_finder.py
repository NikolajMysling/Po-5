import cv2 as cv
import numpy as np
import os

from Kingdomino_pointmodel import find_clusters

# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"King_Domino_dataset\62.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            print(get_terrain(tile))
            print("=====")
            

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# Determine the type of terrain in a tile
def get_terrain(tile):
    hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
    hue, saturation, value = np.median(hsv_tile, axis=(0,1)) # Consider using median instead of mean
    print(f"H: {hue}, S: {saturation}, V: {value}")
    if 22 < hue < 27 and 235 < saturation < 256 and 157 < value < 199:
        return "Field"
    if 33 < hue < 61 and 77 < saturation < 226 and 32 < value < 65:
        return "Forest"
    if 104 < hue < 110 and 223 < saturation < 256 and 114 < value < 185:
        return "Lake"
    if 33 < hue < 46 and 201 < saturation < 246 and 101 < value < 157:
        return "Grassland"
    if 18 < hue < 27 and 51 < saturation < 162 and 78 < value < 124:
        return "Swamp"
    if 21 < hue < 25 and 50 < saturation < 133 and 22 < value < 65:
        return "Mine"
    if 20 < hue < 35 and 50 < saturation < 111 and 72 < value < 142:
        return "Home"
    return "Unknown"

if __name__ == "__main__":
    main()

# ...existing code...

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def visualize_board(terrain_grid, clusters):
    terrain_colors = {
        "Field": "#ffe066",
        "Forest": "#228B22",
        "Lake": "#3399ff",
        "Grassland": "#98fb98",
        "Swamp": "#8fbc8f",
        "Mine": "#b0b0b0",
        "Home": "#ffb347",
        "Unknown": "#cccccc"
    }

    fig, ax = plt.subplots(figsize=(6, 6))
    for y, row in enumerate(terrain_grid):
        for x, terrain in enumerate(row):
            color = terrain_colors.get(terrain, "#cccccc")
            rect = plt.Rectangle((x, 4-y), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(x+0.5, 4-y+0.5, terrain[0], ha='center', va='center', fontsize=8, color='black')

    # Tegn clusters med forskellige farver
    for i, (terrain, cluster) in enumerate(clusters):
        for (x, y) in cluster:
            ax.plot(x+0.5, 4-y+0.5, 'o', color='red', markersize=8, alpha=0.5)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticks(range(6))
    ax.set_yticks(range(6))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title("Kingdomino Bræt Visualisering")
    ax.set_aspect('equal')

    # Legende
    legend_patches = [mpatches.Patch(color=color, label=terrain) for terrain, color in terrain_colors.items()]
    plt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# ...existing code...

def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    
    image_path = r"King_Domino_dataset\58.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return

    image = cv.imread(image_path)
    tiles = get_tiles(image)

    # Lav grid med terræner
    terrain_grid = []
    for y, row in enumerate(tiles):
        terrain_row = []
        for x, tile in enumerate(row):
            terrain_type = get_terrain(tile)
            terrain_row.append(terrain_type)
        terrain_grid.append(terrain_row)

    # Find sammenhængende felter
    clusters = find_clusters(terrain_grid)
    print("\nSammenhængende områder på brættet:")
    for terrain, cluster in clusters:
        print(f"{terrain}: {len(cluster)} felter -> {cluster}")

    # Visualiser brættet og clusters
    visualize_board(terrain_grid, clusters)

if __name__ == "__main__":
    main()
# ...existing code...