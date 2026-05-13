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

    @field_validator('zones', mode="after")
    def zone_validator(zones: List[Zone]) -> List[Zone]:
        if len(zones) < 2:
            raise ValueError("Too few zones")
        names = {}
        for zone in zones:
            try:
                names[zone.name] += 1
            except Exception:
                names[zone.name] = 1
        for _, number in names.items():
            if number != 1:
                raise ValueError("Similar names")

    @field_validator('connections', mode="after")
    def connections_validator(connections: List[Connection]) -> List[Connection]:
        connections = {}
        for connection in connections:
                try:
                    connections[(connection.from_str, connection.to_str)] += 1
                except Exception:
                    connections[(connection.from_str, connection.to_str)] = 1
                try:
                    connections[(connection.to_str, connection.from_str)] += 1
                except Exception:
                    connections[(connection.to_str, connection.from_str)] = 1
        for _, number in connections.items():
            if number != 1:
                raise ValueError("Similar connections")
        return connections
# -----------------------------------------------------------------------------------
# config file lines verif
class Connection_line(BaseModel):
    line: str
    @field_validator('line', mode="after")
    def connection_line_validator(connection_line: str) -> str:
        connection = connection_line.split(":")
        if len(connection) != 2:
            raise ValueError(f"Line {connection_line} has too many ':'")
        





















