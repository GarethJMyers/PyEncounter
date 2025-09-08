from src.Entity.EntityBasic import EntityBasic

class EntityEnemy(EntityBasic):
    """
    Expanded entity. This class also tracks an entity's maximum HP, current HP, and temporary HP.
    Includes methods for damaging/healing the entity, and setting temporary hit points.

    Current hit points and temporary hit points must be >= 0 at all times.
    Max hit points must be > 0

    How damaging works:
    - If entity has temporary hit points, take them down to zero before affecting the current hit points.
    - If entity has no temporary hit points, reduce current hit points until they are zero.

    How healing works:
    - If entity is current health is max, cannot heal.
    - Can only heal current health, healing cannot affect temporary HP.
    - Can only heal up to maximum HP.

    How temporary HP works:
    - Temporary HP cannot be increased, it can only be set to a certain amount, then reduced by taking damage.
    - Can be reduced down to 0.

    If the maximum HP is changed to a value lower than the current HP, the current HP is reduced to the new
    maximum HP.

    When setting maximum HP, if the new value is not greater than 0, an error is raised.
    When setting current HP, if the new value is negative, no error is raised. Instead, it is set to 0.
    When setting temporary HP, if the new value is negative, no error is raised. Instead, it is set to 0.

    Calling the "damage" method when the entity does not meet the requirements to take damage has no effect.
    Calling the "heal" method when the entity does not meet the requirements to be healed has no effect.
    """

    def __init__(self, entity_name: str, short_code: str, initiative: int, max_hp: int):
        if max_hp <= 0:
            raise AssertionError("Maximum HP for entity " + entity_name + " must be greater than zero.")

        self.__max_hp = max_hp
        self.__current_hp = max_hp
        self.__temp_hp = 0
        super().__init__(entity_name, short_code, initiative)

    def set_max_hp(self, new_max_hp: int):
        if new_max_hp <= 0:
            raise AssertionError("Tried to change maximum HP for entity " + self.__name + " but the new value was " +
                                 "less than zero.")
        self.__max_hp = 0
        if self.__current_hp > new_max_hp:
            self.__current_hp = new_max_hp

    def set_current_hp(self, new_hp: int):
        if new_hp < 0:
            self.__current_hp = 0
        else:
            self.__current_hp = new_hp

    def set_temp_hp(self, new_temp_hp: int):
        if new_temp_hp < 0:
            self.__temp_hp = 0
        else:
            self.__temp_hp = new_temp_hp

    def get_max_hp(self):
        return self.__max_hp

    def get_current_hp(self):
        return self.__current_hp

    def get_temp_hp(self):
        return self.__temp_hp

    def heal(self, heal_amount: int):
        self.__current_hp = min(
            self.__max_hp,
            self.__current_hp + heal_amount
        )

    def damage(self, damage_amount: int):
        if self.__temp_hp > 0:
            if self.__temp_hp > damage_amount:
                self.set_temp_hp(self.__temp_hp - damage_amount)
            else:
                old_temp = self.get_temp_hp()
                self.set_temp_hp(0)
                to_damage_current = damage_amount - old_temp
                self.damage(to_damage_current)
        else:
            self.__current_hp = max(0, self.__current_hp - damage_amount)

    def export_dict(self):
        base_dict = super().export_dict()
        base_dict["Class"] = "EntityEnemy"
        for i in [
            {"Max HP": self.__max_hp},
            {"Current HP": self.__current_hp},
            {"Temp HP": self.__temp_hp}
        ]:
            base_dict.update(i)
        return base_dict
