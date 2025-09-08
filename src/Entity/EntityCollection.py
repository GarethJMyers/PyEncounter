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

    The entity objects are kept in a dictionary. The keys for the dictionary are the short codes, therefore short codes
    cannot be reused. Names can be reused, however.

    The object is initialised to not contain any entities. Entities must be added after initialisation.

    The parameter "turn order" is a list of every short code, in the turn order. ie. the first entity in the turn order
    is the zeroth element of the list.
    """

    def __init__(self):
        self.__entities = {}
        self.__turn_order = []
        self.__initiatives = []
        self.__round = 0

    def add_entity(
        self,
        entity: Union[EntityBasic, EntityEnemy, EntityCharges, EntityLegendary]
    ):
        scode = entity.get_short_code()
        initiative = entity.get_initiative()
        self.__entities.update({scode: entity})
        if len(self.__turn_order) == 0:
            self.__turn_order.append(scode)
            self.__initiatives.append(initiative)
        elif GLOBAL_SETTINGS["AddNewEntityUnder"]:
            # add turn order to after last turn order with same/greater initiative
            init_greater_equal = [initiative < i for i in self.__initiatives]
            if not True in init_greater_equal:
                # all existing initiatives are less than new one, so add to top.
                self.__turn_order.insert(0, scode)
                self.__initiatives.insert(0, initiative)
            else:
                # new initiative is not highest, so need to add in middle or end
                for i in reversed(range(len(init_greater_equal))):
                    if init_greater_equal[i]:
                        new_pos = i + 1
