from parsing.config_models import Options, Coord, Zone, Connection
from parsing.parser import ConfigLoader
from pydantic import ValidationError

def main():
    try:
        parser = ConfigLoader()
        parser.load_config("maps/easy/01_linear_path.txt")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
