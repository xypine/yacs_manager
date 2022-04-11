import toml

yacs_path = "../../"

def yacs_c_c_path():
    return f"{yacs_path}yacs_components.toml"

def parseData():
    data = toml.load(yacs_c_c_path())
    return data

def writeData(data):
    with open(yacs_c_c_path(), "w") as f:
        toml.dump(data, f)

def getComponents():
    data = parseData()
    if "components" in data:
        return data["components"]
    return []

def setComponents(components):
    data = parseData()
    data["components"] = components
    writeData(data)

def addComponent(component):
    if "name" in component and "pull_url" in component and "run" in component:
        oldcomp = getComponents()
        oldcomp.append(component)
        print(f"New components: {oldcomp}")
        setComponents(oldcomp)
        return True
    else:
        return False