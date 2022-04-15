import subprocess

def restart():
    print("User requested a system reboot...")
    ps = subprocess.run(["reboot"])
    print(f"Reboot status: {ps.returncode}")
    if ps.returncode != 0:
        return False
    return True