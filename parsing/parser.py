from .config_models import Options, Connection, Coord, Zone, ConfigError
from typing import Union


class ConfigLoader():
    def __init__(self):
        pass

    def load_config(self, config_file: str) -> None:
        if self._check_filename(config_file) is not True:
            raise ConfigError(str(self._check_filename(config_file)))
        try:
            lines = []
            zones = []
            with open(config_file, "r") as file:
                for line in file:
                    lines.append(line)
            if not lines[0].startswith("nb_drones: "):
                raise ConfigError("Number of drones param doesnt exist/isn't at first line")
            nb_drones = lines[0].split(": ")[1]
            index = 1
            while lines[index] == "\n":
                index += 1
            try:
                while lines[index]:
                    if lines[index].startswith("start_hub") or lines[index].startswith("hub") or lines[index].startswith("end_hub"):
                        zones.append(self._get_hub_infos(lines[index]))
                    index += 1
            except Exception as e:
                print(e)

        except Exception as e:
            raise ConfigError("test")
    def _get_hub_infos(self, line: str) -> Zone:
        params_dict = {
            "type": "normal",
            "color": "None",
            "max_drones": 1
        }
        strip_line = line.split(" ", 4)
        name = strip_line[1]
        coo_x = strip_line[2]
        coo_y = strip_line[3]
        coord = Coord(coord_x = coo_x, coord_y = coo_y)
        if len(strip_line) == 5:
            params = strip_line[4].split(" ")
            for param in params:
                
                params_dict[param.strip(" ,[]").split("=")[0]] = param.strip(" ,[]\n").split("=")[1]
        zone = Zone(name = name, coords = coord, type = params_dict["type"], color = params_dict["color"], max_drones = params_dict["max_drones"])
        return zone

    def _get_connection_infos(self, line: str) -> Connection:
        params_dict = {
            "max_link_capacity": 1
        }


    def _check_filename(self, config_file: str) -> Union[bool, str]:
        try:
            file = open(config_file, "r")
        except Exception as e:
            return e
        return True
