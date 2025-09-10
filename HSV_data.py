import cv2 as cv
import numpy as np
import os
import csv

# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"C:\Users\mmads\Documents\UNI\1. Semester\Code\AAU-DAKI-2025\King_Domino_dataset\1.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return

    image = cv.imread(image_path)
    tiles = get_tiles(image)

    # Gem tile data i en CSV-fil
    save_tile_data(tiles)

    print(f"Der er gemt HSV-data for {len(tiles)*len(tiles[0])} tiles i 'tile_data.csv'.")

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# Save HSV values from all tiles into a CSV file
def save_tile_data(tiles):
    i = 1
    while os.path.exists(f"tile_data_{i}.csv"):
        i += 1
    filename = f"tile_data_{i}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["x", "y", "hue", "saturation", "value"])
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
                h, s, v = np.median(hsv_tile, axis=(0, 1))
                writer.writerow([x, y, h, s, v])

    print(f"HSV-data gemt i: {filename}")


if __name__ == "__main__":
    main()
