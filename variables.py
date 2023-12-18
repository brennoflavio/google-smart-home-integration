import os
from dotenv import load_dotenv

load_dotenv()


def load_and_assert(variable):
    var = os.getenv(variable)
    assert var, f"Failed to retreive the following env var: {variable}"
    return var
