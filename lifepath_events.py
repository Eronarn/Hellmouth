# Contains all lifepath events.
# 'age' (int)       : Age category the event fits into. Also broken up by comments.
# 'name' (str)      : Display name during character generation. Defaults to key name.
# 'text' (str)      : Display text during character generation.
# 'short' (str)     : Alternate short text during character dumps.
# 'effects' (dict)  : Dictionary of skill/advantage changes caused by the event.
# 'years' (int)     : Number of years the event takes duirng character generation.
# 'choices' (tuple) : Tuple of choices for progression from this lifepath.
eventdata = {
# Start of data
# Age 0: Parents (~-9 months old)
'Mundane Parents' : {
    'age'     : 0,
    'text'    : "My parents were regular people like yourself.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 1: Infant (0 years old)
'Mundane Infant' : {
    'age'     : 1,
    'text'    : "My birth was exciting for my parents, but few others.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Dark Omen' : {
    'age'     : 1,
    'text'    : "Dark omens troubled the day of my birth.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Strange Omen' : {
    'age'     : 1,
    'text'    : "Eerie signs were seen on the day of my birth.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Holy Day' : {
    'age'     : 1,
    'text'    : "I was born on a holy day.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Bloody Birth' : {
    'age'     : 1,
    'text'    : "I was born on the battlefield.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
'Immediate Adoption' : {
    'age'     : 1,
    'text'    : "I was given up right after birth - unwanted by my own mother.",
    'effects' : {},
    'years'   : 2,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: Who raised you? ('Immediate Adoption')
'Church Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Age 2: Young Child (~2 years old)
'Mundane Young Child' : {
    'age'     : 2,
    'text'    : "My early years were uneventful.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Rich Young Child' : {
    'age'     : 2,
    'text'    : "I spent my early years swaddled in cloth-of-gold.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Young Child' : {
    'age'     : 2,
    'text'    : "Even as an infant, I was deprived of what I needed in life.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Stolen Young Child' : {
    'age'     : 2,
    'text'    : "I was stolen away from my parents.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Orphaned Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth, my parents were brutally killed.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: Did you stay with who raised you? ('Immediate Adoption')
'Church Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: What were you stolen by? ('Stolen Young Child')
'Changeling Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Cultist Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: What killed your parents? ('Young Child')
'Pirate Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Bandit Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wolf Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: What kind of odd behaviors? ('Odd Young Child')
'Magical Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Bookish Young Child' : {
    'age'     : 2,
    'text'    : "Soon after my birth I began to exhibit odd behaviors.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},

# Age 3: Child (~8 years old)
'Mundane Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Rich Child' : {
    'age'     : 3,
    'text'    : "Fortune smiled upon me as a young child.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Child' : {
    'age'     : 3,
    'text'    : "Fortune spat upon me as a young child.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Child' : {
    'age'     : 3,
    'text'    : "I had an uneventful childhood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Child' : {
    'age'     : 3,
    'text'    : "Separated from the civilization of my birth, my upbringing was unusual indeed.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Child' : {
    'age'     : 3,
    'text'    : "Even the few friends I had as a child considered me to be queer.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: Who were you raised by? ('Immediate Adoption', enlisted or rescued)
# FORK: How were you wild? ('Wild Child')
# FORK: How were you odd? ('Odd Child')

# Age 4: Teen (~14 years old)
'Mundane Teen' : {
    'age'     : 4,
    'text'    : "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Dedicated Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to labor from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Scoundrel Teen' : {
    'age'     : 4,
    'text'    : "I turned my efforts to sin from a young age, and I learned much from my experiences.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Teen' : {
    'age'     : 4,
    'text'    :  "My years as a teenager were tumultuous - but who isn't that true of?",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Teen')
# FORK: How were you odd? ('Odd Teen')

# Age 5: Young Adult (~20 years old)
'Mundane Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Rich Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Young Adult' : {
    'age'     : 5,
    'text'    : "My life was quiet as I grew into adulthood.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Young Adult')
# FORK: How were you odd? ('Odd Young Adult')

# Age 6: Adult (>25 years old)
'Mundane Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Rich Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Poor Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Enlisted Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Wild Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Odd Adult' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# FORK: How were you trained? ('Immediate Adoption', rescued, or enlisted)
# FORK: How were you wild? ('Wild Adult')
# FORK: How were you odd? ('Odd Adult')

# FORK: How did you get into demon-slaying?
'Reluctant Demonslayer' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Vengeful Demonslayer' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Zealous Demonslayer' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Violent Demonslayer' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Curious Demonslayer' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
'Corrupt Demonslayer' : {
    'age'     : 6,
    'text'    :  "As an adult, little troubled me.",
    'effects' : {},
    'years'   : 1,
    'choices' : ('', '', '', '', '', ''),
},
# Not supported at this time:
# Age 7: Middle Age (>40 years old)
# Close of data
}

if __name__ == "__main__":
    for k, v in eventdata.iteritems():
        print k