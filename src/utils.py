import os
import platform


def get_os_config():
    cwd = os.getcwd()
    slash = "/"
    if platform.system() == "Windows":
        slash = "\\"
    return cwd, slash


def create_directory(path):
    if isinstance(path, list):
        cwd, slash = get_os_config()
        path = slash.join(path)
        path = f"{cwd}{slash}{path}"

    try:
        os.mkdir(path)
    except FileExistsError:
        print(f"{path} directory was already created")
    except OSError:
        print(f"Creation of the {path} directory failed due to os restrictions")
    else:
        print(f"{path} directory created")
