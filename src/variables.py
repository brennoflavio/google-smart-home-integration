import os

def load_and_assert(variable):
    var = os.getenv(variable)
    assert var, f"Failed to retreive the following env var: {variable}"
    return var

def load(variable):
    var = os.getenv(variable)
    return var
