class Parser():
    def __init__(self) -> None:
        self.content = ""

    def open(self, filename: str) -> None:
        print(filename)
        with open(filename, "r") as f:
            self.content = f.read()
    def process(self) -> dict:
        res = []
        parser = ParserManager()
        lines = self.content.split("\n")
        file_line = 1
        i = 0
        for line in lines:
            if not line.startswith("#") and len(line):
                try:
                    res.append(parser.process(line))
                except ValidationError as e:
                    raise ValueError(f"[{file_line}] - {e.errors()[0]['msg']}")
                except Exception as e:
                    raise ValueError(f"[{file_line}] - {e}")

                i += 1
            if i == 1:
                if res[0]["parser"] != "drone_count":
                    raise ValueError(
                        f"[{file_line}] - Number of drone must be at the first"
                        " line of the file"
                    )
            file_line += 1
        return res


def SpecificParser(ABC):
    @abstractmethod
    def process(line: str) -> dict:
        pass


def DroneCountParser(SpecificParser):
    def __init__(self) -> None:
        self._regex = re.compile(r"^nb_drones:\s+(?P<nbr>\d+)", re.M)

    def process(line: str) -> dict:
        match = self._regex.match(line)
        if not match:
            raise ValueError("Error: Invalid Line")
        obj = match.groupdict()
        obj["nbr"] = int(obj["nbr"])
        return obj

class HubParser():
    def __init__(self) -> None:
        # Regex pour capturer le type (hub/start/end), le nom, x, y et les extras
        self._regex = re.compile(
            r"^(?P<h_type>hub|start_hub|end_hub):\s+(?P<name>\w+)\s+(?P<x>\-?\d+)\s+(?P<y>\-?\d+)(?P<extra>.*)$",
            re.M
        )

    def process(self, line: str) -> Zone:
        match = self._regex.match(line)
        if not match:
            raise ValueError("Error: Invalid line")

            data = match.groupdict()
            h_type = data['h_type']

        extra_tags = {}
        if data["extra"]:
            tags = re.finditer(r"(?P<key>\w+)=(?P<value>\w+)", data["extra"])
            for t in tags:
                extra_tags[t.group("key")] = t.group("value")


class ParserManager():
    def __init__(self) -> None:
        _parsers = []


