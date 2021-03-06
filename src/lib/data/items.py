# TODO: Garrotes
# TODO: Ranged combat
# TODO: Nets
# TODO: Kicks (and other techniques)
# TODO: Lances
# TODO: Whips
# TODO: Foreign weapons

# TODO: Better way of storing/etc. this data
from src.lib.util.define import *
from src.lib.objects.items.item import *

item_list = {
# Swords.
    "broadsword" : {
        "class" : Broadsword,
        "cost" : 500,
        "weight" : 3,
        "attack_options" : {
            "Broadsword" : [
                #  0      1        2      3      4      5       6
                # name, damage, d.type, reach, parry, min ST, hands
                ("swing", "sw+1", "cut", (1,), 0, 10, 1),
                ("thrust", "thr+1", "cr", (1,), 0, 10, 1),
            ],
        },
    },
    "thrusting broadsword" : {
        "class" : Broadsword,
        "cost" : 600,
        "weight" : 3,
        "attack_options" : {
            "Broadsword" : [ # Dmg., type, reach, parry, min ST, hands
                ("swing", "sw+1", "cut", (1,), 0, 10, 1),
                ("thrust", "thr+2", "imp", (1,), 0, 10, 1),
            ],
        },
    },
    "bastard sword" : {
        "class" : Broadsword,
        "cost" : 650,
        "weight" : 5,
        "primary_skill" : "2H Sword",
        "attack_options" : {
            "Broadsword" : [
                ("swing", "sw+1", "cut", (1,2), U0, 11, 1),
                ("thrust", "thr+1", "cr", (2,), U0, 11, 1),
            ],
            "2H Sword" : [
                ("swing", "sw+2", "cut", (1,2), 0, 10, 2),
                ("thrust", "thr+2", "cr", (2,), 0, 10, 2),
            ],
        },
    },
    "thrusting bastard sword" : {
        "class" : Broadsword,
        "cost" : 750,
        "weight" : 5,
        "primary_skill" : "2H Sword",
        "attack_options" : {
            "Broadsword" : [
               ("swing", "sw+1", "cut", (1,2), U0, 11, 1),
               ("thrust", "thr+2", "imp", (2,), U0, 11, 1),
            ],
            "2H Sword" : [
               ("swing", "sw+2", "cut", (1,2), 0, 10, 2),
               ("thrust", "thr+3", "imp", (2,), 0, 10, 2),
            ],
        },
    },
    "greatsword" : {
        "class" : Broadsword,
        "cost" : 800,
        "weight" : 7,
        "primary_skill" : "2H Sword",
        "attack_options" : {
            "2H Sword" : [
               ("swing", "sw+3", "cut", (1,2), 0, 12, 2),
               ("thrust", "thr+2", "cr", (2,), 0, 12, 2),
            ],
        },
    },
    "thrusting greatsword" : {
        "class" : Broadsword,
        "cost" : 900,
        "weight" : 7,
        "primary_skill" : "2H Sword",
        "attack_options" : {
            "2H Sword" : [
               ("swing", "sw+3", "cut", (1,2), 0, 12, 2),
               ("thrust", "thr+3", "imp", (2,), 0, 12, 2),
            ],
        },
    },
# Short blades.
    "shortsword" : {
        "class" : Shortsword,
        "cost" : 400,
        "weight" : 2,
        "attack_options" : {
            "Shortsword" : [
               ("swing", "sw", "cut", (1,), 0, 8, 1),
               ("thrust", "thr", "imp", (1,), 0, 8, 1),
            ],
        },
    },
# Knives and daggers.
    "small knife" : {
        "class" : Knife,
        "cost" : 30,
        "weight" : .5,
        "attack_options" : {
            "Knife" : [
               ("swing", "sw-3", "cut", (0,1), -1, 5, 1),
               ("thrust", "thr-1", "imp", (0,), -1, 5, 1),
            ],
        },
    },
    "large knife" : {
        "class" : Knife,
        "cost" : 40,
        "weight" : 1,
        "attack_options" : {
            "Knife" : [
               ("swing", "sw-2", "cut", (0,1), -1, 6, 1),
               ("thrust", "thr", "imp", (0,), -1, 6, 1),
            ],
        },
    },
    "dagger" : {
        "class" : Dagger,
        "cost" : 20,
        "weight" : .25,
        "attack_options" : {
            "Knife" : [("thrust", "thr-1", "imp", (0,), -1, 5, 1)],
        },
    },

# Axes.
    "hatchet" : {
        "class" : Axe,
        "cost" : 40,
        "weight" : 2,
        "attack_options" : {
            "Axe/Mace" : [("swing", "sw", "cut", (1,), 0, 8, 1)]
        },
    },
    "axe" : {
        "class" : Axe,
        "cost" : 50,
        "weight" : 4,
        "attack_options" : {
            "Axe/Mace" : [("swing", "sw+2", "cut", (1,), U0, 11, 1)]
        },
    },
    "throwing axe" : {
        "class" : Axe,
        "cost" : 60,
        "weight" : 4,
        "attack_options" : {
            "Axe/Mace" : [("swing", "sw+2", "cut", (1,), U0, 11, 1)]
        },
    },
    "greataxe" : {
        "class" : Axe,
        "cost" : 100,
        "weight" : 8,
        "primary_skill" : "2H Axe/Mace",
        "attack_options" : {
            "2H Axe/Mace" : [("swing", "sw+3", "cut", (1,2), U0, 12, 3)]
        },
    },

# Maces.

    "small mace" : {
        "class" : Mace,
        "cost" : 35,
        "weight" : 3,
        "attack_options" : {
            "Axe/Mace" : [("swing", "sw+2", "cr", (1,), U0, 10, 1)]
        },
    },

    "mace" : {
        "class" : Mace,
        "cost" : 50,
        "weight" : 5,
        "attack_options" : {
            "Axe/Mace" : [("swing", "sw+3", "cr", (1,), U0, 12, 1)]
        },
    },

# Picks, hammers, and sickles.
    "sickle" : {
        "class" : Pick,
        "cost" : 15,
        "weight" : 2,
        "attack_options" : {
            "Axe/Mace" : [
                ("slice", "sw", "cut", (1,), 0, 8, 1),
                ("swing", "sw", "imp", (1,), U0, 8, 1),
#                ("hook", "thr-2", "cut", (1,), U0, 8, 1),
            ],
        },
    },
    "pick" : {
        "class" : Pick,
        "cost" : 70,
        "weight" : 3,
        "attack_options" : {
            "Axe/Mace" : [("swing", "sw+1", "imp", (1,), U0, 10, 1)]
        },
    },
    "maul" : {
        "class" : Hammer,
        "cost" : 80,
        "weight" : 12,
        "primary_skill" : "2H Axe/Mace",
        "attack_options" : {
            "2H Axe/Mace" : [("swing", "sw+4", "cr", (1,2), U0, 12, 3)],
        },
    },
    "warhammer" : {
        "class" : Pick,
        "cost" : 100,
        "weight" : 7,
        "primary_skill" : "2H Axe/Mace",
        "attack_options" : {
            "2H Axe/Mace" : [("swing", "sw+3", "imp", (1,2), U0, 12, 3)],
        },
    },

# Clubs.

    "baton" : {
        "class" : Club,
        "cost" : 20,
        "weight" : 1,
        "primary_skill" : "Shortsword",
        "attack_options" : {
            "Shortsword" : [
               ("swing", "sw", "cr", (1,), 0, 6, 1),
               ("thrust", "thr", "cr", (1,), 0, 6, 1),
            ],
        },
    },
    "light club" : {
        "class" : Club,
        "cost" : 5,
        "weight" : 3,
        "attack_options" : {
            "Broadsword" : [
               ("thrust", "thr+1", "cr", (1,), 0, 10, 1),
               ("swing", "sw+1", "cr", (1,), 0, 10, 1),
            ],
        },
    },

# Flails.

    "morningstar" : {
        "class" : Flail,
        "cost" : 80,
        "weight" : 6,
        "attack_options" : {
            "Flail" : [("swing", "sw+3", "cr", (1,), U0, 12, 1)],
        },
    },
    "flail" : {
        "class" : Flail,
        "cost" : 100,
        "weight" : 8,
        "primary_skill" : "2H Flail",
        "attack_options" : {
            "2H Flail" : [("swing", "sw+4", "cr", (1,2), U0, 13, 2)],
        },
    },
# Long battlefield polearms.
    "glaive" : {
        "class" : Pollaxe,
        "cost" : 100,
        "weight" : 8,
        "attack_options" : {
            "Polearm" : [
               ("chop", "sw+3", "cut", (2,3), U0, 11, 3),
               ("thrust", "thr+3", "imp", (1,2,3), U0, 11, 2),
            ],
        },
    },
    "halberd" : {
        "class" : Pollaxe,
        "cost" : 150,
        "weight" : 12,
        "attack_options" : {
            "Polearm" : [
               ("chop", "sw+5", "cut", (2,3), U0, 13, 3),
               ("swing", "sw+4", "imp", (2,3), U0, 13, 3),
               ("thrust", "thr+3", "imp", (1,2,3), U0, 12, 2),
            ],
        },
    },
    "poleaxe" : {
        "class" : Pollaxe,
        "cost" : 120,
        "weight" : 10,
        "attack_options" : {
            "Polearm" : [
               ("chop", "sw+4", "cut", (2,3), U0, 12, 3),
               ("thrust", "sw+4", "cr", (2,3), U0, 12, 3),
            ],
        },
    },

# Shorter polearms.

    "dueling pollaxe" : {
        "class" : Pollaxe,
        "cost" : 100,
        "weight" : 8,
        "attack_options" : {
            "Polearm" : [
               ("chop", "sw+3", "cut", (1,2), U0, 11, 3),
               ("thrust", "sw+3", "cr", (1,2), U0, 11, 3),
            ],
        },
    },

# Spears.
    "spear" : {
        "class" : Spear,
        "cost" : 40,
        "weight" : 4,
        "attack_options" : {
            "Spear" : [
               ("thrust", "thr+2", "imp", (1,), 0, 9, 1),
               ("thrust", "thr+3", "imp", (1,2), 0, 9, 2),
            ],
        },
    },
    "long spear" : {
        "class" : Spear,
        "cost" : 60,
        "weight" : 5,
        "attack_options" : {
            "Spear" : [
               ("thrust", "thr+2", "imp", (2,3), U0, 10, 1),
               ("thrust", "thr+3", "imp", (2,3), 0, 10, 2),
            ],
        },
    },
    # Unimplemented: -2 to hit, Target at -1 to Dodge, +1 to Block or Parry.
    "trident" : {
        "class" : Spear,
        "cost" : 80,
        "weight" : 5,
        "attack_options" : {
            "Spear" : [
               ("thrust", "thr+3", "imp", (1,), U0, 11, 1),
               ("thrust", "thr+4", "imp", (1,2), 0, 10, 2),
            ],
        },
    },

# Staves

    "quarterstaff" : {
        "class" : Staff,
        "cost" : 10,
        "weight" : 4,
        "attack_options" : {
            "Staff" : [
               ("swing", "sw+2", "cr", (1,2), 2, 7, 2),
               ("thrust", "thr+2", "cr", (1,2), 2, 7, 2),
            ],
            "2H Sword" : [
               ("swing", "sw+2", "cr", (1,2), 0, 9, 2),
               ("thrust", "thr+1", "cr", (2,), 0, 9, 2),
            ],
        },
    },

# Unarmed-augmentors.

    "brass knuckles" : {
        "cost" : 10,
        "weight" : .25,
        "attack_options" : {
           "Boxing"   : [("thrust", "thr", "cr", (0,), 0, None, None)],
           "Brawling" : [("thrust", "thr", "cr", (0,), 0, None, None)],
           "Karate"   : [("thrust", "thr", "cr", (0,), 0, None, None)],
           "DX"       : [("thrust", "thr", "cr", (0,), 0, None, None)],
        },
    },

    "blackjack" : {
        "class" : Weapon,
        "cost" : 20,
        "weight" : 1,
        "attack_options" : { # Damage, type, reach, parry, min ST
           "Brawling" : [("hit", "thr", "cr", (0,), 0, 7, 1)],
           "DX"       : [("hit", "thr", "cr", (0,), 0, 7, 1)],
        },
    },

# Small improvised weapons.

    "wooden stake" : {
        "class" : Weapon,
        "cost" : 4,
        "weight" : .5,
        "attack_options" : {
           "Knife" : [("thrust", "thr(.05)", "imp", (0,), -1, 5, 1)],
        },
    },

    "chain" : {
        "variant" : "flail",
    },

# Small farm tools.

    "trowel" : {
        "variant" : "dagger",
    },

    "machete" : {
        "variant" : "shortsword",
    },

    "pruning shears" : {
        "variant" : "small knife",
    },

    "hedge trimmers" : {
        "variant" : "shortsword",
    },

# Small shop tools.

    "pliers" : {
        "variant" : "dagger",
    },

    "screwdriver" : {
        "variant" : "dagger",
    },

    "auger" : {
        "variant" : "dagger",
    },

    "wrench" : {
        "variant" : "small mace",
    },

    "claw hammer" : {
        "class" : Pick,
        "cost" : 70,
        "weight" : 3,
        "attack_options" : {
            "Axe/Mace" : [
                ("swing", "sw+1", "cr", (1,), U0, 10, 1),
                ("swing", "sw", "imp", (1,), U0, 10, 1)
            ]
        },
    },

    "ball-peen hammer" : {
        "variant" : "small mace",
    },

# Large improvised weapons.

    "scythe" : {
        "class" : Tool,
        "cost" : 15,
        "weight" : 5,
        "attack_options" : {
            "2H Axe/Mace" : [
               ("swing", "sw+2", "cut", (1,), U0, 11, 3),
               ("swing", "sw", "imp", (1,), U0, 11, 3),
            ],
        },
    },

    "pitchfork" : {
        "variant" : "trident",
    },

    "wood ax" : {
        "variant" : "greataxe",
    },

    "mattock" : {
        "variant" : "warhammer",
    },

    "hoe" : {
        "variant" : "dueling pollaxe",
    },

    "shovel" : {
        "class" : Tool,
        "cost" : 80,
        "weight" : 5,
        "primary_skill" : "2H Axe/Mace",
        "attack_options" : {
            "2H Axe/Mace" : [("swing", "sw+2", "cr", (1,2), U0, 12, 3)],
        },
    },

    "rake" : {
        "class" : Pollaxe,
        "cost" : 100,
        "weight" : 3,
        "attack_options" : {
            "Polearm" : [
               ("swing", "sw+1", "imp", (1,2), U0, 11, 3),
               ("swing", "sw+1", "cr", (1,2), U0, 11, 3),
            ],
        },
    },

# Fake items.

# Natural attacks.

    "fist" : {
        "class" : Natural,
        "attack_options" : { # Damage, type, reach, parry, min ST
            "Boxing"   : [("punch", "thr-1", "cr", (0,), 0, None, None)],
            "Brawling" : [("punch", "thr-1", "cr", (0,), 0, None, None)],
            "Karate"   : [("punch", "thr-1", "cr", (0,), 0, None, None)],
            "DX"       : [("punch", "thr-1", "cr", (0,), 0, None, None)],
        },
    },

    # TODO: work this into advantage

    "sharp claws" : {
        "class" : Natural,
        "attack_options" : { # Damage, type, reach, parry, min ST
            "Boxing"   : [("claw", "thr-1", "cut", (0,), 0, None, None)],
            "Brawling" : [("claw", "thr-1", "cut", (0,), 0, None, None)],
            "Karate"   : [("claw", "thr-1", "cut", (0,), 0, None, None)],
            "DX"       : [("claw", "thr-1", "cut", (0,), 0, None, None)],
        },
    },

    "blunt teeth" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : [("bite", "thr-1", "cr", (0,), None, None, None)],
            "DX"       : [("bite", "thr-1", "imp", (0,), None, None, None)],
        },
    },
    "sharp teeth" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : [("bite", "thr-1", "cut", (0,), None, None, None)],
            "DX"       : [("bite", "thr-1", "cut", (0,), None, None, None)],
        },
    },
    "fangs" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : [("bite", "thr-1", "imp", (0,), None, None, None)],
            "DX"       : [("bite", "thr-1", "imp", (0,), None, None, None)],
        },
    },
    "beak" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : [("peck", "thr-1", "pi+", (0,), None, None, None)],
            "DX"       : [("peck", "thr-1", "pi+", (0,), None, None, None)],
        },
    },
# TODO: A ton of demonic strikers. Tails, wings, etc.
# TODO: Shield bashes.

    "armor" : {
        "class" : Armor,
        "dr" : 1,
        "slots" : ["Neck", "Torso", "RArm", "LArm"]
    },

    "leggings" : {
        "class" : Armor,
        "dr" : 1,
        "slots" : ["RLeg", "LLeg", "Groin"]
    },

    "gloves" : {
        "class" : Armor,
        "dr" : 1,
	"slots" : ["RHand", "LHand"]
    },

    "boots" : {
        "class" : Armor,
        "dr" : 1,
        "slots" : ["RFoot", "LFoot"]
    },

    "breastplate" : {
        "class" : Armor,
        "dr" : 5,
        "slots" : ["Torso"]
    },
    "gauntlets" : {
        "variant" : "gloves",
        "dr" : 2,
    },
}
'''
LEG:

upper
    padded - cuisse
    brigandine - cuisse
    mail - short chauss, cuisse
    plate - cuisse
knee
    plate - poleyn
lower
    plate - schynbald
    plate - greave

upper+knee
    mail - short chauss

upper+knee+lower
    mail - chauss

CHAUSS:
  upper, lower?, knee?
  padded, mail

CUISSE:
  upper, knee?
  padded, leather, plate

GREAVE:
  lower leg
  plate

SCHYNBALD (demi-greaves):
  lower leg
  plate (front only)

SABATON/SOLLERET:
  foot
  plate

TASSET:
  upper
  plate

COUTER:
  elbow
  plate

GAUNTLET: (mitten vs. finger)
  hand
  anything

PAULDRON:
  shoulder + armpit
  plate

SPAULDER:
  shoulder
  plate

REREBRACE:
  upper arm
  splint, plate

VAMBRACE:
  lower arm
  leather, plate

BRACER:
  lower arm
  leather (archery)

VEST:
  torso, abdomen
  brigandine

DOUBLET:
  torso, arms
  brigandine

GAMBESON: (arming doublet if under plate). might extend to cover thighs
  torso, arms
  cloth

CUIRASS: (breastplate + backplate)
  torso
  any RIGID

CORSLET:
  torso + neck + arms + gauntlets

FAULD:
  abdomen
  plate (?)

HAUBERK:
  torso, arms, upper legs, knee (?)
  mail

HAUBERGEON / MAIL SHIRT:
  torso, upper arms
  mail

BIRNIE:
torso, 

Above can come in HOODED versions.

CODPIECE:
  groin
  leather, plate

COLLAR: (can be integrated into a mail shirt or worn seperate)
  neck
  rigid mail

BEVOR:
  neck, throat
  plate

GORGET:
  neck, throat
  leather, plate

COIF:
  head/neck/shoulders, or attached to mail shirt
  mail

GUSSETS:
1) Fifteenth-century mail sleeves covering the armpits and other portions of the arm not covered by plate armor

Half armor (see also corselet)
Armor for the the torso and arms, but leaving the legs unprotected
'''


# Test code.
if __name__ == '__main__':
    swords = ("broadsword", "katana")
    for sword in swords:
        stats = item_list[sword]
        if stats.get("variant") is not None:
            stats = item_list[stats["variant"]]
        sword = stats["class"]()
        for stat, value in stats.items():
            print stat, value
            setattr(sword, stat, value)
        print sword.__dict__
