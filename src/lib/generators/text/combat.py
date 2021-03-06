from src.lib.util.dice import *
from src.lib.util.text import *

from src.lib.generators.text.describe import describe

def combat(attack):
    strings = []

    # Hit and did 0 or more points of injury.
    if attack.get("injury") is not None:

        if attack.get("retreat position") is not None:
            strings.append("%s tries to jump back!" % attack["target"].appearance())

        # Damage level tokens
        if attack.get("dismembering_wound") is not None:
            damage_level = "dismember"
        elif attack.get("crippling_wound") is not None:
            damage_level = "cripple"
        # HACK: Torsos and the like can't be crippled, but should still
        # display gorier damage messages when hit for large amounts of damage.
        # TODO: Replace this with better information (e.g., overpenetration)
        elif attack["wound"] > 2 * attack["target"].MaxHP():
            damage_level = "dismember"
        elif attack["wound"] > attack["target"].MaxHP():
            damage_level = "cripple"
        elif attack.get("major_wound") is not None:
            damage_level = "wound"
        elif attack["wound"] > 1:
            damage_level = "injure"
        elif attack["wound"] == 1:
            damage_level = "scratch"
        else:
            damage_level = "none"

        wound = ""
        punctuation = "."

        if attack.get("dismembered") is not None:
            wound = ", maiming it"
            punctuation = "!"
            if attack.get("dismembering_wound") is True and attack["damage_type"] == "cut":
                attack["severing_wound"] = True
                wound = ", severing it"
        elif attack.get("crippled") is not None:
            wound = ", crippling it"
            punctuation = "!"
        elif attack.get("major_wound") is not None:
            punctuation = "!"

        # TODO: Have other kinds of basic strings.
        string = "%s @dmg-%s-%s-%s@ %s's %s%s%s" % (attack["attacker"].appearance(), damage_level, attack["damage_type"], attack["attack_name"], attack["defender"].appearance(), attack["location"].appearance(), wound, punctuation)

        # DEBUG:
        #formula = "%s, [%s = (%s-%s)*%s]" % (attack["injury"], attack["wound"], attack["basic damage"], attack["basic damage blocked"], attack["multiplier"])
        #string += " {"+formula+"}"

        strings.append(string)

        # Shouting if a major wound
        # TODO: Check to not cry out
        # TODO: Move out of this file.
        if attack.get("major_wound") is not None:
            if attack["defender"].voice is not None and attack["defender"].get("Status", "unconscious") is False:
                strings.append("%s @%s-dmg-%s@!" % (attack["defender"].appearance(), attack["defender"].voice, damage_level))

    # Hit, but the target defended.
    elif attack.get("defense_check") > TIE:
        # Defense level tokens
        margin = attack["defense_margin"]
        punctuation = "."

        # Critical successes
        if attack["defense_check"] == CRIT_SUCC:
            defense_level = "crit-"
            punctuation = "!"
            if margin >= 6:
                defense_level += "trivial"
            elif margin >= 4:
                defense_level += "easy"
            elif margin >= 2:
                defense_level += "normal"
            elif margin >= 1:
                defense_level += "hard"
            elif margin == 0:
                defense_level += "difficult"
            # If your roll only succeeded because it was a crit :D
            else:
                defense_level += "insane"
        # Normal successes
        else:
            if margin >= 6:
                defense_level = "trivial"
                punctuation = "!"
            elif margin >= 4:
                defense_level = "easy"
            elif margin >= 2:
                defense_level = "normal"
            elif margin == 1:
                defense_level = "hard"
            else:
                defense_level = "difficult"
                punctuation = "!"

        if attack.get("retreat position") is not None:
            defense_level += "-retreat"

        strings.append("%s @def-%s-%s@ %s's %s%s" % (attack["defender"].appearance(), attack["defense_name"], defense_level, attack["attacker"].appearance(), attack["attack_name"], punctuation))

    # Miss!
    else:
        margin = attack["attack_margin"]
        punctuation = "."
        # Critical misses
        if attack["attack_check"] == CRIT_FAIL:
            miss_level = "crit-"
            punctuation = "!"
            if margin <= -6:
                miss_level += "difficult"
            elif margin <= -4:
                miss_level += "hard"
            elif margin <= -2:
                miss_level += "normal"
            elif margin <= -1:
                miss_level += "easy"
            # If your roll only failed because it was a crit :D
            else:
                miss_level += "unlucky"
        # Normal successes
        else:
            if margin <= -6:
                miss_level = "difficult"
                punctuation = "!"
            elif margin <= -4:
                miss_level = "hard"
            elif margin <= -2:
                miss_level = "normal"
            elif margin == -1:
                miss_level = "easy"
            else: # Should never happen?
                miss_level = "unlucky"
                punctuation = "!"

        strings.append("%s @miss-%s@ %s%s" % (attack["attacker"].appearance(), miss_level, attack["defender"].appearance(), punctuation))

    formatted = []
    for string in strings:
        formatted.append(describe(string))
    return formatted
