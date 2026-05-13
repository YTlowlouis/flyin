from .config_models import Options, Connection, Coord, Zone, ConfigError
from typing import Union


class ConfigLoader():
    def __init__(self):
        self.config_file: str

    def load_config(self, config_file: str) -> None:
        if self._check_filename(config_file) is not True:
            raise ConfigError(str(self._check_filename(config_file)))

        self.config_file = config_file
        try:
            lines = []
            zones = []
            connections = []

            with open(config_file, "r") as file:
                for line in file:
                    lines.append(line)

            if not lines[0].startswith("nb_drones: "):
                raise ConfigError("Number of drones param does not exist/isn't at first line")

            nb_drones = lines[0].split(": ")[1]

            index = 1

            while index < len(lines):
                if (
                    lines[index].startswith("start_hub")
                    or lines[index].startswith("hub")
                    or lines[index].startswith("end_hub")
                ):
                    zones.append(self._get_hub_infos(lines[index], index))
                    print(zones[-1])
                elif lines[index].startswith("connection"):
                    connections.append(self._get_connection_infos(lines[index], index))
                elif lines[index] == "\n":
                    pass
                else:
                    self.return_error("Invalid line", index)
                index += 1

        except Exception as e:
            self.return_error(str(e), index)
        print(zones, connections)

    def _get_hub_infos(self, line: str, line_index: int) -> Zone:
        params_dict = {
            "type": "normal",
            "color": "None",
            "max_drones": 1
        }
        try:
            strip_line = line.split(maxsplit=4)
            name = strip_line[1]
            coo_x = int(strip_line[2])
            coo_y = int(strip_line[3])
            coord = Coord(coord_x = coo_x, coord_y = coo_y)
            if len(strip_line) == 5:
                params = strip_line[4].split(" ")
                for param in params:
                    params_dict[param.strip(" ,[]").split("=")[0]] = param.strip(" ,[]\n").split("=")[1]
            zone = Zone(name = name, coords = coord, line = line_index, type = params_dict["type"], color = params_dict["color"], max_drones = params_dict["max_drones"])
        except Exception as e:
            raise Exception(f"Error {e}")
        return zone

    def _get_connection_infos(self, line: str, line_index: int) -> Connection:
        params_dict = {
            "max_link_capacity": 1
        }
        newline = line.split(maxsplit = 2)
        if len(newline != 3) and len(newline) != 2:
            self.return_error("invalid line", line_index)
        fromm, to = tuple(newline[1].split(": ", maxsplit=1))
        if len(newline) == 3:
            if not newline[2].startswith("[") or newline[2].endswith("]"):
                params = newline[2].strip("[]").split(", ")
                if len(params) != 1:
                    self.return_error("Too many params", line_index)
                if params[0].split("=", maxsplit=1)[0] != "max_link_capacity":
                    self.return_error("Invalid parameter", line_index)
                try:
                    params_dict[params[0].split("=", maxsplit=1)[0]] = int(params[0].split("=", maxsplit=1)[1])
                except Exception:
                    self.return_error("Invalid max_link_capacity", line_index)
                connection = Connection(from_str = fromm, to_str= to, max_link_capacity = params_dict["max_link_capacity"])
                return connection

    def _check_filename(self, config_file: str) -> Union[bool, str]:
        try:
            with open(config_file, "r"):
                pass
        except Exception as e:
            return e
        return True

    def return_error(self, error_msg: str, line_index: int) -> None:
        with open(self.config_file, "r") as f:
            lines = []
            for line in f:
                lines.append(line)
       # print("test")
        error = f"Error at line {str(line_index + 1)}: {lines[line_index]}, {error_msg}"
        raise ConfigError(error)

