from parsing.parser2 import MapLoader

def main():
    maploader = MapLoader()
    print(maploader.load("maps/easy/01_linear_path.txt"))

if __name__ == "__main__":
    main()
