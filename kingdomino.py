import cv2 as cv #bruges til billedbehandling (f.eks. læse filer, ændre farverum og klippe billeder)
import numpy as np #bruges til matematiske beregniner af gennemsnit af pixels
import os #bruges til at arbejde med filer og tjekke om de findes


# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"King_Domino_dataset\1.jpg" #definerer en sti til billedet
    if not os.path.isfile(image_path): #tjekker om filen findes. hvis den ikke findes, så print "Image not found" og afslut programmet
        print("Image not found")
        return

    # 🔹 Start farvevælgeren
    color_picker_mode(image_path)
#    image = cv.imread(image_path) #læser billedet fra den definerede sti, som en matrix af pixels.
#    tiles = get_tiles(image) #deler billedet op i små matricer (tiles)
#    print(len(tiles))
#    for y, row in enumerate(tiles):
#        for x, tile in enumerate(row):
#            print(f"Tile ({x}, {y}):")
#            print(get_terrain(tile))
#            print("=====") #efter endt, så looper den igennem alle tiles og printer deres koordinater og hvad den mener terrænet er.

# Break a board into tiles he
def get_tiles(image):
    tiles = []
    for y in range(5): #brættet opdeles i 5x5 tiles = 25 felter. hver tile er 100x100 pixels. 
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles   #returnerer en liste af lister, hvor hver indre liste repræsenterer en række af tiles på brættet.
#den skærer altså billedet op i 25 mindre billeder. så en slags grid slicing. resultatet er en 2d liste hvor hvert element er en lille billede matrice


# Determine the type of terrain in a tile
def get_terrain(tile): #først konverteres billedet fra BGR til HSV farverum. lettere at skelne farver i HSV end i BGR.
    hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
    hue, saturation, value = np.mean(hsv_tile, axis=(0,1)) # Consider using median instead of mean. - np.mean tager gennemsnittet af alle pixels i tilen. den giver et gennemsnittal for hue, saturation og value.
    print(f"H: {hue}, S: {saturation}, V: {value}")
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Field"
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Forest"
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Lake"
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Grassland"
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Swamp"
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Mine"
    if 0 < hue < 0 and 0 < saturation < 0 and 0 < value < 0:
        return "Home"
    return "Unknown" #værdier er ikke indsat. der for returner den unknown.
# meningen er at vi skal sætte de rigtige farveinterfaller ind i if statements, så den kan genkende de forskellige terræntyper. (eks. Hue: 30-40 =gult = field).

# Hjælpefunktion: klik på et billede og få HSV-værdier 
def pick_color(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:  # venstre klik med musen
        hsv = cv.cvtColor(param, cv.COLOR_BGR2HSV)
        pixel = hsv[y, x]
        print(f"Klik på ({x},{y}) -> H: {pixel[0]}, S: {pixel[1]}, V: {pixel[2]}")

# Kør farvevælger til at indsamle data
def color_picker_mode(image_path):
    img = cv.imread(image_path)
    if img is None:
        print("Kunne ikke åbne billedet")
        return
    cv.imshow("Board", img)
    cv.setMouseCallback("Board", pick_color, img)
    print("Klik på et felt i vinduet for at se HSV-værdier (tryk på en tast for at lukke).")
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main() 
#systemet bestemmer terræn ud fra farverne i hver tile.