# Functions for writing and loading settings.
# Settings are saved in JSON format for readability

# These settings are all things that should be configurable by the user. FOr things that should not be configurable,
# use GLOBAL_VARS.py.

# Due to the JSON format storing all keys as strings, all keys in the dictionary must be strings.

# Settings keys:
#   - "AddNewEntityUnder": If True (default), when a new entity is added that has the same initiative as other entities
#   that have already been added, add it beneath those entities. If False, add it above.

from json import dump, load
import pathlib as pl
from os import remove

SETTINGS_FILE_PATH = "../../GlobalSettings.json"
SETTINGS_FILE_PL = pl.Path(SETTINGS_FILE_PATH)

def default_settings():
    """
    Deletes the global settings file (if it exists) and generates a new one with default values.
    """
    if SETTINGS_FILE_PL.is_file():
        remove(SETTINGS_FILE_PL)
    settings_dict = {
        "AddNewEntityUnder": True
    }
    with open(SETTINGS_FILE_PL, "w") as file:
        dump(
            obj=settings_dict,
            fp=file
        )

def read_settings():
    """
    Reads the settings file. If it doesn't exist, initialise a default settings file first.
    Returns the settings dictionary.
    """
    if not SETTINGS_FILE_PL.is_file():
        default_settings()
    with open(SETTINGS_FILE_PL, "r") as file:
        return_dict = load(file)
    return return_dict

GLOBAL_SETTINGS = read_settings()