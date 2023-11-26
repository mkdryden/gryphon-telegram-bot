import logging
from abc import ABC, abstractproperty, abstractmethod
from random import choice, choices, random


class BaseFood(ABC):
    success_grab_text = ['{gryphon} swooped down and nabbed a {food}', '{gryphon} grabbed a {food}',
                         '{gryphon} caught a {food}', '{gryphon} hunted a {food}', '{gryphon} snatched a {food}']

    success_eating_text = [' and ate it!', ' and gobbled it up!', ' and ate it in one bite!',
                           ' and ate it in two bites!', ' and devoured it!', ' and ate it with a side of fries!',
                           ' and turned it into a sandwich!']

    fail_grab_text = ['{gryphon} swooped down and missed a {food}', '{gryphon} missed a {food}',
                      '{gryphon} failed to catch a {food}', '{gryphon} failed to hunt a {food}']

    fail_eating_text = [' and it got away!', ' and it escaped!', ' and it ran away!',
                        ' and fell into an undignified heap!', ' and went hungry!', ', it was too fast!',
                        ', it was too quick!', ', it was too smart!', ', it was too clever!',
                        ', tripping over its shoelaces!', ', falling for a Nigerian prince scam!', ]

    fail_death_text = [', but became its lunch instead!', ' and fell down a hole and died!', ' and died of shame!',
                       ' and died of embarrassment!', ' and broke its neck falling down the stairs!',
                       ' and died of dysentery!', ' and died of scurvy!', ]

    def __init__(self, name: str, category: str = 'Small to medium sized mammal',
                 rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.05):
        self.name = name
        self.category = category
        self.rarity: float = rarity  # 0.0 - 1.0
        self.success_rate: float = success_rate
        self.death_chance = death_chance

    def __repr__(self):
        return f"Food({self.name})"

    def hunt(self, name: str) -> tuple[bool, str]:
        """
        Hunt for this food
        :param name: Name of the gryphon
        :return: Tuple of (died, message)
        """

        if random() < self.success_rate:
            return False, self.hunt_success().format(gryphon=name, food=self.name)
        else:
            died, msg = self.hunt_fail()
            return died, msg.format(gryphon=name, food=self.name)

    def hunt_success(self) -> str:
        return f"{choice(self.success_grab_text)}{choice(self.success_eating_text)}"

    def hunt_fail(self) -> tuple[bool, str]:
        if random() < self.death_chance:
            return True, f"{choice(self.fail_grab_text)}{choice(self.fail_death_text)}"
        return False, f"{choice(self.fail_grab_text)}{choice(self.fail_eating_text)}"


class SmallMammal(BaseFood):
    def __init__(self, name: str, rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.05):
        super().__init__(name, category='Small mammal', rarity=rarity, success_rate=success_rate,
                         death_chance=death_chance)


class Bird(BaseFood):
    fail_death_text = BaseFood.fail_death_text + [' and died of bird flu!', ' and died of avian flu!',
                                                 ' and got pecked to death!', ' and got chirped to death!',
                                                 ' and got tweeted to death!', ' and got screeched to death!',
                                                 ' and got bored to death!']

    def __init__(self, name: str, rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.05):
        super().__init__(name, category='Birds and Bird Eggs', rarity=rarity, success_rate=success_rate,
                         death_chance=death_chance)


class BirdEgg(BaseFood):
    success_eating_text = BaseFood.success_eating_text + [' and turned it into an omlette!',
                                                          ' and turned it into a cake!',
                                                          ' and turned it into a souffle!',
                                                          ' and turned it into merengue!', ]
    fail_grab_text = ['{gryphon} swooped down and missed a {food}', '{gryphon} missed a {food}',
                      '{gryphon} failed to catch a wiley {food}']
    fail_eating_text = [', distracted by a shiny object!', ', clearly outmatched in cunning!', ]
    fail_death_text = [', and slipped on a banana peel and died!', ', and died in a freak juggling accident!']

    def __init__(self, name: str, rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.01):
        super().__init__(name, category='Birds and Bird Eggs', rarity=rarity, success_rate=success_rate,
                         death_chance=death_chance)


class Fish(BaseFood):
    success_eating_text = BaseFood.success_eating_text + ['and turned it into sushi!',
                                                         'and turned it into a fish taco!',
                                                         'and turned it into a fish sandwich!',
                                                         'and turned it into a fish burger!', ]
    fail_eating_text = BaseFood.fail_eating_text + [', it was too slippery!', ', it was too slimy!',
                                                   ', it was too wet!', ', it was too fishy!', ]
    fail_death_text = BaseFood.fail_death_text + [', and drowned!', ', and died of hypothermia!',
                                                 ', and died of ciguaterra poisoning at a sketchy sushi restauraunt!', ]

    def __init__(self, name: str, rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.02):
        super().__init__(name, category='Fish', rarity=rarity, success_rate=success_rate, death_chance=death_chance)


class Livestock(BaseFood):
    success_eating_text = BaseFood.success_eating_text + [' and turned it into a steak!',
                                                          ' and turned it into a burger!',
                                                          ' and turned it into a hot dog!',
                                                          ' and turned it into a meatloaf!', ]

    fail_death_text = BaseFood.fail_death_text + [', and got trampled to death!', ', and got kicked to death!',
                                                  ', and got gored to death!', ', and got mauled to death!',
                                                  ', and got eaten by a nearby dragon!', ]

    def __init__(self, name: str, rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.05):
        super().__init__(name, category='Livestock', rarity=rarity, success_rate=success_rate,
                         death_chance=death_chance)


class Mythical(BaseFood):
    success_eating_text = BaseFood.success_eating_text + ['and turned it into a steak!',
                                                          ' and turned it into a burger!',
                                                          ' and turned it into a hot dog!',
                                                          ' and turned it into a meatloaf!', ]

    fail_death_text = BaseFood.fail_death_text + [", and got magick'd™ to death!", ", and got cursed to death!", ]

    def __init__(self, name: str, rarity: float = 0.5, success_rate: float = 0.5, death_chance: float = 0.08):
        super().__init__(name, category='Mythical Creatures', rarity=rarity, success_rate=success_rate,
                         death_chance=death_chance)


class Dragon(BaseFood):
    fail_grab_text = ['{gryphon} foolishly attacked a {food}', '{gryphon} had the audacity to attack a {food}',
                      '{gryphon}, in a moment of madness, attacked a {food}',
                      '{gryphon}, ignoring all sense of self-preservation, attacked a {food}']

    fail_death_text = [' and got roasted to death!', ' and got burned to death!', ' and got flambéed to death!',
                       ' and was made into katsu!', ' and was made into a kebab!', ' and was made into a burger!',
                       ' and was made into stew!', ' and was made into a pie!', ' and was made into a sandwich!',
                       ' and was cooked to the perfect medium-rare!', ' and was served as a side dish!',
                       ' and made for a great snack!', ' and made for a delicious entreé!',
                       ' and made for a tasty appetizer!', ]

    def __init__(self, name: str, rarity: float = 0.1, success_rate: float = 0., death_chance: float = 1, ):
        super().__init__(name, category='Mythical Creatures', rarity=rarity, success_rate=success_rate,
                         death_chance=death_chance)


class DragonEgg(Dragon):
    fail_grab_text = ['{gryphon} foolishly attacked a {food}, but ran into mommy',
                      '{gryphon} had the audacity to attack a {food}, but ran into daddy',
                      '{gryphon} found a seemingly undefended {food}, but got caught under a box propped up by'
                      ' a stick',
                      '{gryphon}, ignoring all sense of self-preservation, attacked a {food}, but got caught in a net']


class BabyDragon(DragonEgg):
    pass


class Foods(object):
    def __init__(self, foods: list[BaseFood]):
        self.foods = foods
        self.categories: dict[str] = {i.category: None for i in self.foods}  # Use dict to maintain order
        self.foods_by_category = {i: [j for j in self.foods if j.category == i]
                                  for i in self.categories}

    def get_food(self, category: str = None) -> BaseFood:
        if category is None:
            return choices(self.foods, weights=[i.rarity for i in self.foods], k=1)[0]
        else:
            return choices(self.foods_by_category[category],
                           weights=[i.rarity for i in self.foods_by_category[category]], k=1)[0]


foods = Foods(
    [SmallMammal('rabbit', rarity=0.5, success_rate=0.8),
     SmallMammal('squirrel', rarity=0.5, success_rate=0.8),
     SmallMammal('fawn', rarity=0.5, success_rate=0.7),
     Bird('chicken', rarity=0.7, success_rate=0.8),
     Bird('duck', rarity=0.5, success_rate=0.8),
     Bird('cassowary', rarity=0.1, success_rate=0.8, death_chance=0.2),
     BirdEgg('chicken egg', rarity=0.7, success_rate=0.8),
     BirdEgg('duck egg', rarity=0.5, success_rate=0.8),
     BirdEgg('ostrich egg', rarity=0.1, success_rate=0.8, death_chance=0.1),
     Fish('salmon', rarity=0.5, success_rate=0.6),
     Fish('tuna', rarity=0.2, success_rate=0.6),
     Fish('shark', rarity=0.1, success_rate=0.3, death_chance=0.1),
     Livestock('cow', rarity=0.5, success_rate=0.7),
     Livestock('pig', rarity=0.7, success_rate=0.8),
     Livestock('sheep', rarity=0.3, success_rate=0.5),
     Mythical('unicorn', rarity=0.2, success_rate=0.3, death_chance=0.07),
     Mythical('phoenix', rarity=0.2, success_rate=0.3, death_chance=0.1),
     Mythical('hippogriff', rarity=0.2, success_rate=0.3, death_chance=0.1),
     Mythical('gryphon', rarity=0.1, success_rate=0.3, death_chance=0.2),
     Dragon('dragon', rarity=0.1),
     Dragon('young dragon', rarity=0.1, death_chance=0.9),
     DragonEgg('dragon egg', rarity=0.1),
     BabyDragon('dragon hatchling', rarity=0.1),
     ]
)
