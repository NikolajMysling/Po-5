import cv2 as cv
import numpy as np
import os

# ---------------------------
# Terrænkodning baseret på HSV
# ---------------------------
def get_terrain(tile):
    hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
    hue, saturation, value = np.median(hsv_tile, axis=(0,1))
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

# ---------------------------
# Del billedet op i 5x5 tiles
# ---------------------------
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# ---------------------------
# Find sammenhængende felter
# ---------------------------
def find_clusters(board):
    visited = [[False]*len(board[0]) for _ in range(len(board))]
    clusters = []

    def dfs(x, y, terrain, cluster):
        if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
            return
        if visited[y][x]:
            return
        if board[y][x] != terrain:
            return
        visited[y][x] = True
        cluster.append((x, y))
        # Naboer: op, ned, venstre, højre
        dfs(x+1, y, terrain, cluster)
        dfs(x-1, y, terrain, cluster)
        dfs(x, y+1, terrain, cluster)
        dfs(x, y-1, terrain, cluster)

    for y in range(len(board)):
        for x in range(len(board[0])):
            if not visited[y][x]:
                cluster = []
                dfs(x, y, board[y][x], cluster)
                if cluster:
                    clusters.append((board[y][x], cluster))
    return clusters

# ---------------------------
# Main
# ---------------------------
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    
    image_path = r"C:\Users\mmads\Documents\UNI\1_Semester\Code\AAU-DAKI-2025\King_Domino_dataset\1.jpg"
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

if __name__ == "__main__":
    main()
