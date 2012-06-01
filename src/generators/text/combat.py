from dice import *
from generators.text.describe import describe

def combat(attack):
    if attack.get("damage done") is not None:
        formula = "%s [(%s-%s)*%s]" % (attack["damage done"], attack["damage rolled"], attack["damage blocked"], attack["multiplier"])
        string = "%s @dmg-%s-%s@ %s in the %s for %s" % (attack["attacker"].appearance(), attack["damage type"], attack["attack option"], attack["target"].appearance(), attack["location"].appearance(), formula)

        spikes = attack.get("reciprocal damage done")
        if spikes is not None:
            string += " @dmg-spike@ %s" % spikes

    elif attack.get("defense-check") == SUCC:
        string = "%s @def@ %s" % (attack["target"].appearance(), attack["attacker"].appearance())
    else:
        string = "%s @miss@ %s" % (attack["attacker"].appearance(), attack["target"].appearance())

    return describe(string)
