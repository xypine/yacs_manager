import subprocess
import toml

yacs_path = "../../../"
yacs_exec = "../../../yacs.x86_64"

def yacs_c_c_path():
    return f"{yacs_path}yacs_components.toml"

def parseData():
    global yacs_path, yacs_exec
    data = toml.load(yacs_c_c_path())
    if "yacs" in data:
        yacs_config = data["yacs"]
        print(f"Yacs config found: {yacs_config}")
        if "path" in yacs_config and yacs_config['path'] != yacs_path:
            print(f"Setting yacs path from {yacs_path} to {yacs_config['path']}")
            yacs_path = yacs_config["path"]
        if "exec" in yacs_config and yacs_config['exec'] != yacs_exec:
            print(f"Setting yacs exec from {yacs_exec} to {yacs_config['exec']}")
            yacs_exec = yacs_config["exec"]
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

def removeComponent(component_name):
    newcomp = []
    oldcomp = getComponents()
    for c in oldcomp:
        if c["name"] != component_name:
            newcomp.append(c)
    setComponents(newcomp)
    return True

def updateComponents():
    subprocess.run([f"{yacs_exec}", "update-components"])
    return True