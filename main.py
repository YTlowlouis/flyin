from parsing.parser2 import MapLoader
from parsing.config_models import ConfigError

def main():
    loader = MapLoader()
    try:
        result = loader.load("maps/easy/01_linear_path.txt")
        print(*result, end="\n")
    except ConfigError as e:
        print(f"ConfigError: {e}")

if __name__ == "__main__":
    main()
