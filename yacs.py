from os import kill
import subprocess
import toml

yacs_path = "../../.."
yacs_exec = "../../../yacs.x86_64"

def yacs_c_c_path():
    return f"{yacs_path}/yacs_components.toml"

def parseData():
    global yacs_path, yacs_exec
    data = toml.load(yacs_c_c_path())
    if "paths" in data:
        yacs_pathconfig = data["paths"]
        # print(f"Yacs paths config found: {yacs_pathconfig}")
        if "main" in yacs_pathconfig and yacs_pathconfig['main'] != yacs_path:
            print(f"Setting yacs path from {yacs_path} to {yacs_pathconfig['main']}")
            yacs_path = yacs_pathconfig["main"]
        if "exec" in yacs_pathconfig and yacs_pathconfig['exec'] != yacs_exec:
            print(f"Setting yacs exec from {yacs_exec} to {yacs_pathconfig['exec']}")
            yacs_exec = yacs_pathconfig["exec"]
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
    print("Updating components with yacs...")
    subprocess.run([f"{yacs_exec}", "update-components"])
    return True

def restartComponents():
    killComponents()
    print("Restarting yacs...")
    subprocess.run([f"{yacs_exec}", "run-components"])
    return True

def killComponents():
    pname = yacs_exec.split("/")[-1]
    print(f"Killing all processes with the name \"{pname}\" (and any children of those processes)")
    pid = subprocess.run(["pgrep", "-f", f"{pname}"], capture_output=True)
    print("pid search command output: ", pid.stdout)
    print("pid search errors: ", pid.stderr)
    if pid.returncode != 0:
        return False
    pid = pid.stdout.decode("UTF-8").strip()
    print(f"Killing yacs (pid {pid}) by user command...")
    ps = subprocess.run(["kill", "-SIGINT", f"-{pid}"], capture_output=True)
    print("Kill command output: ", ps.stdout)
    print("Kill command errors: ", ps.stderr)
    if ps.returncode != 0:
        return False
    return True
