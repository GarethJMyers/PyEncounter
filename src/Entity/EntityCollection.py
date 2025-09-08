from src.Entity.EntityBasic import EntityBasic
from src.Entity.EntityEnemy import EntityEnemy
from src.Entity.EntityCharges import EntityCharges
from src.Entity.EntityLegendary import EntityLegendary
from src.Other.Settings import GLOBAL_SETTINGS

from json import dump, load
from typing import Union

class EntityCollection:
    """
    This class holds the entity objects and can iterate through them. It tracks the turn order, which entity's turn
    it is, and the number of rounds that have passed. When a EntityLegendary's turn comes up, the legendary actions
    are reset. It allows import/export of all data as a json.

    Import can only occur if the entities dictionary is empty.

    Entity objects are stored in a list in the turn order, ie. the first entity in the turn order is the zeroth entity
    in the list. When a new entity is added, it is added to either:
    - after the last entity with a greater or equal initiative
    - before the first entity that has a lesser or equal initiative
    depending on whether the global setting "AddNewEntityUnder" is true or false respectively.

    Note: There is nothing to stop the same entity being added multiple times, or two entities with the same parameters
    being added.
    """

    def __init__(self):
        self.__entities = []

    def add_entity(self, entity: Union[EntityBasic, EntityEnemy, EntityCharges, EntityLegendary]):
        if len(self.__entities) < 1:
            self.__entities.append(entity)
        elif GLOBAL_SETTINGS["AddNewEntityUnder"]:  # add after the last entity with a greater or equal initiative
            last_great_eq = -1
            for i in range(len(self.__entities)):
                if self.__entities[i].get_initiative() >= entity.get_initiative():
                    last_great_eq = i
            self.__entities.insert(last_great_eq + 1, entity)
        else:  # add before the first entity that has a lesser or equal initiative
            first_less_equal = -1
            found_first_less_equal = False
            i = 0
            while (not found_first_less_equal) and (i < len(self.__entities)):
                if self.__entities[i].get_initiative() <= entity.get_initiative():
                    first_less_equal = i
                    found_first_less_equal = True
                i += 1
            first_less_equal = max(0, first_less_equal)
            self.__entities.insert(first_less_equal, entity)
