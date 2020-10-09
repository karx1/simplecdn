import os


def check_env():
    if os.path.isfile("/.containernv"):
        # In container, return user mounted directory
        return "/data"
    else:
        # In dev environment, return local directory
        return "data"

def check_env_bool():
    return os.path.isfile("/.containernv")
