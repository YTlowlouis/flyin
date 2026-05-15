import re
from typing import List, Optional
from pydantic import ValidationError
from .parser import Zone, ConfigError, Connection, Options, Coord

class DroneCountParser:
    """Analyse la ligne initiale déclarant le nombre de drones."""
    def __init__(self) -> None:
        self._regex = re.compile(r"^nb_drones:\s+(?P<nbr>\d+)", re.M)

    def process(self, line: str) -> int:
        match = self._regex.match(line)
        if not match:
            raise ValueError("Format 'nb_drones' invalide")
        return int(match.group("nbr"))

class HubParser:
    """Analyse les lignes de hubs (start, end, ou normal)."""
    def __init__(self) -> None:
        self._regex = re.compile(
            r"^(?P<h_type>hub|start_hub|end_hub):\s+(?P<name>\w+)\s+(?P<x>\-?\d+)\s+(?P<y>\-?\d+)(?P<extra>.*)$",
            re.M
        )

    def process(self, line: str, ln: int) -> Zone:
        match = self._regex.match(line)
        if not match:
            raise ValueError("Format de hub invalide")

        data = match.groupdict()
        h_type = data['h_type']

        extra_tags = {}
        if data["extra"]:
            tags = re.finditer(r"(?P<key>\w+)=(?P<value>\w+)", data["extra"])
            for t in tags:
                extra_tags[t.group("key")] = t.group("value")

        if h_type in ["start_hub", "end_hub"]:
            forbidden = [k for k in ["max_drones", "zone"] if k in extra_tags]
            if forbidden:
                raise ValueError(f"Le {h_type} ne supporte pas les options : {', '.join(forbidden)}")

        return Zone(
            name=data["name"],
            coords=Coord(coord_x=int(data["x"]), coord_y=int(data["y"])),
            line=ln,
            type=extra_tags.get("zone", "normal"),
            color=extra_tags.get("color", "None"),
            max_drones=int(extra_tags.get("max_drones", 1))
        )

class ConnectionParser:
    """Analyse les lignes de liaisons entre les hubs."""
    def __init__(self) -> None:
        self._regex = re.compile(
            r"^connection:\s+(?P<from_str>\w+)-(?P<to_str>\w+)(?P<extra>.*)$", 
            re.M
        )

    def process(self, line: str, ln: int) -> Connection:
        match = self._regex.match(line)
        if not match:
            raise ValueError("Format de connexion invalide")

        data = match.groupdict()

        capacity = 1
        if data["extra"]:
            tags = re.finditer(r"(?P<key>\w+)=(?P<value>\w+)", data["extra"])
            for t in tags:
                if t.group("key") == "max_link_capacity":
                    capacity = int(t.group("value"))

        return Connection(
            from_str=data["from_str"],
            to_str=data["to_str"],
            max_link_capacity=capacity
        )

class MapLoader:
    """Chargeur principal : coordonne la lecture du fichier et la validation finale."""
    def __init__(self):
        self.drone_parser = DroneCountParser()
        self.hub_parser = HubParser()
        self.conn_parser = ConnectionParser()

    def load(self, filename: str) -> Options:
        zones: List[Zone] = []
        connections: List[Connection] = []
        nb_drones: Optional[int] = None

        try:
            with open(filename, 'r') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if nb_drones is None:
                        if not line.startswith("nb_drones:"):
                            raise ConfigError(f"Ligne {i} : 'nb_drones' doit être défini en premier.")
                        nb_drones = self.drone_parser.process(line)
                        continue

                    if any(line.startswith(p) for p in ["hub:", "start_hub:", "end_hub:"]):
                        zones.append(self.hub_parser.process(line, i))

                    elif line.startswith("connection:"):
                        connections.append(self.conn_parser.process(line, i))

                    else:
                        raise ConfigError(f"Ligne {i} : Instruction inconnue ou mal placée.")

            return Options(nb_drones=nb_drones, zones=zones, connections=connections)

        except FileNotFoundError:
            raise ConfigError(f"Le fichier '{filename}' est introuvable.")
        except (ValueError, ValidationError) as e:
            raise ConfigError(f"Erreur de configuration : {e}")
