from src.Entity.EntityEnemy import EntityEnemy
from src.Other.GLOBAL_VARS import MAX_CHARGES

from copy import deepcopy

class EntityCharges(EntityEnemy):
    """
    Extends EntityEnemy to have custom charges.
    The user adds things to track and the maximum number of charges of that thing.
    This class also tracks the charges remaining.

    What charges are tracked are given when the object is initialised. What is tracked cannot be changed after
    initialisation. Max charges cannot be changed after initialisation. The things to be tracked are to be provided as
    a dictionary of: key = name of thing to track, value = maximum number of charges. The maximum number of charges
    must be greater than 0 for every thing to track.

    The remaining number of charges are initialised to zero. If the remaining number of charges is attempted to be
    reduced below zero, nothing happens (no error message).
    """

    def __init__(
        self,
        entity_name: str,
        short_code: str,
        initiative: int,
        max_hp: int,
        charges_to_track: dict[str, int]
    ):
        for key, val in charges_to_track.items():
            if val <= 0:
                raise AssertionError("Tried to intialise EntityCharges with name " + entity_name + ", but the " +
                                     "max charges for " + key + " were zero or less.")

        self.__max_charges = deepcopy(charges_to_track)
        self.__current_charges = deepcopy(charges_to_track)
        super().__init__(entity_name, short_code, initiative, max_hp)

    def reduce_charge(self, charge_name: str):
        """Reduces the number of charges of charge_name by 1."""
        if charge_name not in list(self.__current_charges.keys()):
            raise AssertionError("Tried to reduce the charges for " + charge_name + " for entity " + self.__name +
                                 ", but that is not being tracked for that entity.")

        self.__current_charges[charge_name] = max(0, self.__current_charges[charge_name] - 1)

    def reset_single_charge(self, charge_name:str):
        """Reset the current charges of a single thing back to its maximum."""
        if charge_name not in list(self.__current_charges.keys()):
            raise AssertionError("Tried to reset the charges for " + charge_name + " for entity " + self.__name +
                                 ", but that is not being tracked for that entity.")

        self.__current_charges[charge_name] = self.__max_charges[charge_name]

    def reset_all_charges(self):
        """Resets all charges for the entity."""
        self.__current_charges = self.__max_charges

    def get_charges_single(self, charge_name: str) -> int:
        """Returns the number of charges remaining for a single thing that is tracked."""
        if charge_name not in list(self.__current_charges.keys()):
            raise AssertionError("Tried to return the charges for " + charge_name + " for entity " + self.__name +
                                 ", but that is not being tracked for that entity.")
        return self.__current_charges[charge_name]

    def get_charges_all(self) -> dict[str, int]:
        """Returns dictionary of current charges."""
        return self.__current_charges

    def get_max_charges_single(self, charge_name: str) -> int:
        """Returns the max number of charges remaining for a single thing that is tracked."""
        if charge_name not in list(self.__current_charges.keys()):
            raise AssertionError("Tried to return the charges for " + charge_name + " for entity " + self.__name +
                                 ", but that is not being tracked for that entity.")
        return self.__max_charges[charge_name]

    def get_max_charges_all(self) -> dict[str, int]:
        """Returns dictionary of max charges."""
        return self.__max_charges

    def export_dict(self):
        base_dict = super().export_dict()
        base_dict["Class"] = "EntityCharges"
        base_dict.update({"Max Charges": self.__max_charges})
        base_dict.update({"Current Charges": self.__current_charges})
        return base_dict
