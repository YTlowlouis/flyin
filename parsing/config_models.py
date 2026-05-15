from pydantic import BaseModel, field_validator, ValidationError, model_validator, Field
from typing import Tuple, Optional, List

class ConfigError(Exception):
    pass

#------------------------------------------------------------------------------------
#   CONNECTIONS
class Connection(BaseModel):
    from_str: str
    to_str: str

    #Optional tag
    max_link_capacity: int = Field(Optional=True, default=1, gt=0)
#------------------------------------------------------------------------------------

#   ZONES
class Coord(BaseModel):
    coord_x: int = Field(ge=0)
    coord_y: int = Field(ge=0)

class Zone(BaseModel):
    name: str
    coords: Coord
    line: int

    #Optional tags
    type: str = Field(Optional=True, default="normal")
    color: str = Field(Optional=True, default="None")
    max_drones: int = Field(Optional=True, default=1, ge=0)

    @field_validator('name', mode="after")
    def is_name_valid(name: str) -> str:
        for i in "/\\ ":
            if i in name:
                raise ValueError("Invalid character in zone name")
        return name

    @field_validator('type', mode="after")
    def is_type_valid(type: str) -> str:
        if type not in ["normal", "blocked", "restricted", "priority"]:
            raise ValueError("Invalid type")
        return type

    @field_validator('color', mode="after")
    def is_color_valid(color: str) -> str:
        for i in color:
            if not i.isalpha():
                raise ValueError("Invalid color")
        return color

class Options(BaseModel):
    nb_drones: int = Field(gt=0)
    zones: List[Zone]
    connections: List[Connection]

    @model_validator(mode="after")
    def zone_validator(self) -> List[Zone]:
        names = set()
        for zone in self.zones:
            if zone.name in names:
                raise ValueError(f"Duplicate zone name : {zone.name}")
            names.add(zone.name)
        return self

    @model_validator(mode="after")
    def connections_validator(self) -> List[Connection]:
        seen = set()
        zones = [zone.name for zone in self.zones]
        for conn in self.connections:
            pair = tuple(sorted((conn.from_str, conn.to_str)))
            if pair in seen:
                raise ValueError(f"Duplicate zone name : {pair}")
            fromm, to = pair
            if fromm not in zones or to not in zones:
                raise ValueError(f"Hub in connectin does not exist")
            seen.add(pair)
        return self


# -----------------------------------------------------------------------------------
# config file lines verif
class Connection_line(BaseModel):
    line: str
    @field_validator('line', mode="after")
    def connection_line_validator(connection_line: str) -> str:
        connection = connection_line.split(":")
        if len(connection) != 2:
            raise ValueError(f"Line {connection_line} has too many ':'")
        





















