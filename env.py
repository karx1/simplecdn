import os


def check_env():
    if os.path.isfile("/.dockerenv"):
        # In container, return user mounted directory
        return "/data"
    else:
        # In dev environment, return local directory
        return "data"