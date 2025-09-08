from src.Other.ConditionsDict import conditions_dict
from src.Other.GLOBAL_VARS import MAX_NAME_LEN
from src.Other.GLOBAL_VARS import SCODE_LEN

import string

# list of allowed characters
scode_allowed_chars = list(string.ascii_letters + string.digits) + [" "]

class EntityBasic:
    """
    The Player/Basic Entity class.
    Only tracks Name, Short Code, Initiative, and Conditions.
    Entity name: max 64 characters, all ASCII characters allowed.
    Short code: always 4 characters, if less than 4, then padded with space characters to the right. Only latin
    characters without diacritics, digits, and space characters allowed.
    """
    def __init__(self, entity_name: str, short_code: str, initiative: int):
        # argument validation
        if len(entity_name) > MAX_NAME_LEN:
            raise AssertionError("Tried to create an entity, but its name had more than " + str(MAX_NAME_LEN) +
                                 " characters. Entity name: " + entity_name)
        if len(short_code) > SCODE_LEN:
            raise AssertionError("Tried to create an entity, but its short code had more than " + str(SCODE_LEN) +
                                 " characters. Entity name: " + entity_name)
        for single_char in short_code:
            if single_char not in scode_allowed_chars:
                raise AssertionError("Tried to set short code for entity: " + entity_name + ", but the code contains" +
                                     " the character " + single_char + ", which is not allowed.")

        # set params
        if len(short_code) < SCODE_LEN:
            code_to_use = short_code.ljust(SCODE_LEN)
        else:
            code_to_use = short_code

        self.__name = entity_name
        self.__code = code_to_use
        self.__initiative = initiative
        self.__conds = conditions_dict

    def set_entity_name(self, new_name: str):
        if len(new_name) > MAX_NAME_LEN:
            raise AssertionError("Tried to change entity's name, but its name had more than " + str(MAX_NAME_LEN) +
                                 " characters. Entity name: " + self.__name)
        self.__name = new_name

    def set_short_code(self, new_code: str):
        if len(new_code) > SCODE_LEN:
            raise AssertionError("Tried to change entity's short code, but its name had more than " +
                                 str(SCODE_LEN) + " characters. Entity name: " + self.__name)
        elif len(new_code) < SCODE_LEN:
            code_to_use = new_code.ljust(SCODE_LEN)
        else:
            code_to_use = new_code
        self.__code = code_to_use

    def set_initiative(self, new_init: int):
        self.__initiative = new_init

    def set_condition(self, condition_name: str, set_on: bool):
        if condition_name not in list(self.__conds.keys()):
            raise AssertionError("Tried to set the condition " + condition_name + " for entity " + self.__name +
                                 ", but that condition does not exist in its condition dictionary.")
        self.__conds[condition_name] = set_on

    def get_name(self):
        return self.__name

    def get_short_code(self):
        return self.__code

    def get_initiative(self):
        return self.__initiative

    def get_condition_dict(self):
        return self.__conds

    def get_condition_state(self, condition_name: str):
        if condition_name not in list(self.__conds.keys()):
            raise AssertionError("Tried to get the condition " + condition_name + " for entity " + self.__name +
                                 ", but that condition does not exist in its condition dictionary.")
        return self.__conds[condition_name]

    def export_dict(self):
        """Returns a dictionary of object parameters for serialisation into JSON seperately."""
        return_dict = {
            "ClassType": "Entity",
            "Class": "EntityBasic",
            "Name": self.__name,
            "Short Code": self.__code,
            "Initiative": self.__initiative,
            "Conditions": self.__conds
        }
        return return_dict
