import toml

yacs_path = "../../"

def parseData():
    data = toml.load(f"{yacs_path}yacs_components.toml")
    return data

def getComponents():
    data = parseData()
    if "components" in data:
        return data["components"]
    return []