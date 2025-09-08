from src.Entity.EntityCharges import EntityCharges

class EntityLegendary(EntityCharges):
    """
    Extends EntityCharges. Adds Legendary Actions and Legendary Resistances.
    These work the same as the charges in the parent class, but are tracked seperately so that:
        - They can be displayed seperately in the GUI
        - The legendary actions can be automatically reset at the start of each of the entity's turns.
    The user sets the max charges of legendary actions and legendary resistances.
    These must be zero or greater. If zero, then they are ignored by the GUI.
    """
    
    def __init__(
        self,
        entity_name: str,
        short_code: str,
        initiative: int,
        max_hp: int,
        charges_to_track: dict[str, int],
        num_legendary_actions: int,
        num_legendary_res: int
    ):
        if (num_legendary_actions < 0) or (num_legendary_res < 0):
            raise AssertionError("Tried to set legendary actions/resistances for " + entity_name + ", but they " +
                                 "are less than zero.")
        self.__max_legend_act = num_legendary_actions
        self.__max_legend_res = num_legendary_res
        self.__current_legend_act = num_legendary_actions
        self.__current_legend_res = num_legendary_res
        super().__init__(entity_name, short_code, initiative, max_hp, charges_to_track)

    def get_legend_act(self):
        return self.__current_legend_act

    def get_max_legend_act(self):
        return self.__max_legend_act

    def get_legend_res(self):
        return self.__current_legend_res

    def get_max_legend_res(self):
        return self.__max_legend_res

    def reduce_legend_act(self):
        self.__current_legend_act = max(0, self.__current_legend_act - 1)

    def reduce_legend_res(self):
        self.__current_legend_res = max(0, self.__current_legend_res - 1)

    def reset_legend_act(self):
        self.__current_legend_act = self.__max_legend_act

    def reset_legend_res(self):
        self.__current_legend_res = self.__max_legend_res
        