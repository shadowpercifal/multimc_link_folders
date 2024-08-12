import os
import sys

def safe(terminate: bool):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except:
                if terminate:
                    print(f"Error occured in {function}! Exiting...")
                    os.system("pause")
                    sys.exit()
                else:
                    print(f"Error occured in {function}!")
                    return None
        return wrapper
    return decorator



def safe_mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        return True
    except FileNotFoundError:
        return False
    except:
        return False
    return True