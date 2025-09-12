from src.Entity.EntityBasic import EntityBasic
from src.Entity.EntityEnemy import EntityEnemy
from src.Entity.EntityCharges import EntityCharges
from src.Entity.EntityLegendary import EntityLegendary
from src.Other.Settings import GLOBAL_SETTINGS

from typing import Union

class EntityCollection:
    """
    This class holds the entity objects and can iterate through them. It allows import/export of all data as a json.

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

    def get_entity_names_codes(self):
        """
        Returns a list of tuples. Each tuple is (entity name, entity short code) for an entity. In turn order.
        If no entities, returns empty list.
        """
        return_arr = []
        if len(self.__entities) > 0:
            for i in self.__entities:
                return_arr.append((i.get_name(), i.get_short_code()))
        return return_arr

    def get_entity_initiatives(self):
        """
        Returns a list of tuples. Each tuple is (entity name, entity short code, entity initiative) for an entity.
        In turn order. If no entities, returns empty list.
        """
        return_arr = []
        if len(self.__entities) > 0:
            for i in self.__entities:
                return_arr.append((i.get_name(), i.get_short_code(), i.get_initiative()))
        return return_arr

    def get_single_entity(self, turn_num: int):
        """
        Returns single entity at zeo-indexed turn_num. If turn_num is outside range of entity list, or entity list is
        empty, raises error.
        """
        if len(self.__entities) < 1:
            raise IndexError("Tried to get entities from EntityCollection, but no entities had been added yet.")
        if turn_num >= len(self.__entities):
            raise IndexError("Tried to get entity " + str(turn_num) + " from EntityCollection, but not enough " +
                             "entities had been added.")
        return self.__entities[turn_num]

    def get_num_entities(self) -> int:
        return len(self.__entities)

    def export_dict(self):
        """
        Returns a dictionary containing the details of the entity objects.
        If no entities have been added yet, raise error.
        """
        num_ents = self.get_num_entities()
        if num_ents < 1:
            raise ValueError("Tried to export the entity collection, but it was empty.")
        return_dict = {
            "ClassType": "EntityCollection",
            "NumEntities": num_ents,
            "EntityList": [i.export_dict() for i in self.__entities]
        }
        return return_dict

    def import_dict(self, d: dict):
        """
        Given a dictionary, import entity data.
        If entities have already been added, raise error.
        Expects the dictionary to:
            - Have exactly 3 keys: "ClassType", "NumEntities", and "EntityList".
            - The value of "ClassType" must be "EntityCollection"
            - The "EntityList" must be a list of dictionaries
            - the dictionaries in the list must:
                - have a "ClassType" value that is "Entity".
                - have a "Class" value that is one of "EntityBasic", "EntityEnemy", "EntityCharges", or "EntityLegendary"
        Any deviations from these will result in an error.
        """
        errdesc = ""
        try:
            if d["ClassType"] != "EntityCollection":  # KeyError if not exist
                errdesc = "Not correct ClassType"
                raise KeyError()
            dlist = d["EntityList"]  # KeyError if not exist
            errdesc = "Error with single entity object dictionary"
            for i in dlist:
                if i["ClassType"] != "Entity":  # KeyError if not exist, TypeError if i is not a dict
                    raise KeyError()

                # all 4 classes have these
                ent_name = i["Name"]
                ent_scode = i["Short Code"]
                ent_init = i["Initiative"]
                ent_cond = i["Conditions"]

                # not all classes have these. Set as blank string then try to load
                ent_maxhp = ""
                ent_currhp = ""
                ent_temphp = ""
                ent_maxcharge = ""
                ent_currcharge = ""
                ent_maxlegac = ""
                ent_currlegac = ""
                ent_maxlegres = ""
                ent_currlegres = ""
                try:  # in order, ie. if "Max Charges" isn't a key then the ones under won't be either
                    ent_maxhp = i["Max HP"]
                    ent_currhp = i["Current HP"]
                    ent_temphp = i["Temp HP"]
                    ent_maxcharge = i["Max Charges"]
                    ent_currcharge = i["Current Charges"]
                    ent_maxlegac = i["Max Legendary Actions"]
                    ent_currlegac = i["Current Legendary Actions"]
                    ent_maxlegres = i["Max Legendary Resistances"]
                    ent_currlegres = i["Current Legendary Resistances"]
                except KeyError:
                    pass
                except:
                    errdesc = "Unexpected error when accessing details for one entity."
                    raise KeyError()

                match i["Class"]:
                    case "EntityBasic":
                        new_obj = EntityBasic(
                            entity_name=ent_name,
                            short_code=ent_scode,
                            initiative=ent_init
                        )
                    case "EntityEnemy":
                        new_obj = EntityEnemy(
                            entity_name=ent_name,
                            short_code=ent_scode,
                            initiative=ent_init,
                            max_hp=ent_maxhp
                        )
                        new_obj.set_current_hp(ent_currhp)
                        new_obj.set_temp_hp(ent_temphp)
                    case "EntityCharges":
                        new_obj = EntityCharges(
                            entity_name=ent_name,
                            short_code=ent_scode,
                            initiative=ent_init,
                            max_hp=ent_maxhp,
                            charges_to_track=ent_maxcharge
                        )
                        new_obj.set_all_charges(ent_currcharge)
                        new_obj.set_current_hp(ent_currhp)
                        new_obj.set_temp_hp(ent_temphp)
                    case "EntityLegendary":
                        new_obj = EntityLegendary(
                            entity_name=ent_name,
                            short_code=ent_scode,
                            initiative=ent_init,
                            max_hp=ent_maxhp,
                            charges_to_track=ent_maxcharge,
                            num_legendary_actions=ent_maxlegac,
                            num_legendary_res=ent_maxlegres
                        )
                        new_obj.set_all_charges(ent_currcharge)
                        new_obj.set_current_hp(ent_currhp)
                        new_obj.set_temp_hp(ent_temphp)
                        for j in range(ent_maxlegac - ent_currlegac):
                            new_obj.reduce_legend_act()
                        for j in range(ent_maxlegres - ent_currlegres):
                            new_obj.reduce_legend_res()
                    case _:
                        raise KeyError()
                self.__entities.append(new_obj)
        except KeyError:
            raise AssertionError(errdesc)
        except TypeError:
            raise AssertionError(errdesc)
        except:
            raise AssertionError("Unknown error occurred importing EntityCollection from dict.")
