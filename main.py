from parsing.config_models import Options, Coord, Zone, Connection
from parsing.parser import ConfigLoader
from pydantic import ValidationError

def main():
    try:
        coord = Coord(coord_x=10, coord_y=10)
        zone = Zone(name="start", coords = coord)
        zone2 = Zone(name="end", coords = coord)
        connection = Connection(from_str="start", to_str="end")
        option = Options(nb_drones=2, zones=[zone, zone2], connections=[connection])
        parser = ConfigLoader()
        parser.load_config("maps/easy/01_linear_path.txt")
    except ValidationError as e:
        errors = e.errors()
        print(f"Error at: {errors[0]["input"]}, msg: {errors[0]["msg"]}")

if __name__ == "__main__":
    main()
