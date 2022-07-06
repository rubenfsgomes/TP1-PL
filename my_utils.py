# my_utils.py

def slurp(filename):
    with open(filename, "rt") as fh:
        contents = fh.read()
    return contents

