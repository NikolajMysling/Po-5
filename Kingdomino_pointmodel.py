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
    
    if 21 < hue < 28 and 218 < saturation < 256 and 136< value < 208:
        return "Field"
    if 28 < hue < 80 and 67 < saturation < 226 and 24 < value < 74:
        return "Forest"
    if 103 < hue < 110 and 223 < saturation < 256 and 115 < value < 199:
        return "Lake"
    if 33 < hue < 48 and 159 < saturation < 249 and 75 < value < 165:
        return "Grassland"
    if 17 < hue < 27 and 34 < saturation < 181 and 72 < value < 145:
        return "Swamp"
    if 17 < hue < 26 and 39 < saturation < 156 and 23 < value < 72:
        return "Mine"
    if 16 < hue < 87 and 40 < saturation < 141 and 52 < value < 145:
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

if __name__ == "__main__":
    main()
