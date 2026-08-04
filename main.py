TEXTS = [
    '''Situated about 10 miles west of Kemmerer,
    Fossil Butte is a ruggedly impressive
    topographic feature that rises sharply
    some 1000 feet above Twin Creek Valley
    to an elevation of more than 7500 feet
    above sea level. The butte is located just
    north of US 30 and the Union Pacific Railroad,
    which traverse the valley.''',
    '''At the base of Fossil Butte are the bright
    red, purple, yellow and gray beds of the Wasatch
    Formation. Eroded portions of these horizontal
    beds slope gradually upward from the valley floor
    and steepen abruptly. Overlying them and extending
    to the top of the butte are the much steeper
    buff-to-white beds of the Green River Formation,
    which are about 300 feet thick.''',
    '''The monument contains 8198 acres and protects
    a portion of the largest deposit of freshwater fish
    fossils in the world. The richest fossil fish deposits
    are found in multiple limestone layers, which lie some
    100 feet below the top of the butte. The fossils
    represent several varieties of perch, as well as
    other freshwater genera and herring similar to those
    in modern oceans. Other fish such as paddlefish,
    garpike and stingray are also present.'''
]

USERS = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}

username = input("username: ")
password = input("password: ")

if username not in USERS or USERS[username] != password:
    print("unregistered user, terminating the program..")
    exit()

print("-" * 40)
print(f"Welcome to the app, {username}")
print(f"We have {len(TEXTS)} texts to be analyzed.")
print("-" * 40)

choice = input(f"Enter a number btw. 1 and {len(TEXTS)} to select: ")

if not choice.isdigit():
    print("Invalid input, terminating the program..")
    exit()

choice = int(choice)

if choice < 1 or choice > len(TEXTS):
    print("Invalid input, terminating the program..")
    exit()

text = TEXTS[choice - 1]

for znak in ",.:;!?()-\n":
    text = text.replace(znak, " ")

words = text.split()

titlecase = 0
uppercase = 0
lowercase = 0
numbers = 0
sum_numbers = 0
lengths = {}

for word in words:
    if word.istitle():
        titlecase += 1
    elif word.isupper():
        uppercase += 1
    elif word.islower():
        lowercase += 1

    if word.isnumeric():
        numbers += 1
        sum_numbers += int(word)

    length = len(word)
    lengths[length] = lengths.get(length, 0) + 1

print("-" * 40)
print(f"There are {len(words)} words in the selected text.")
print(f"There are {titlecase} titlecase words.")
print(f"There are {uppercase} uppercase words.")
print(f"There are {lowercase} lowercase words.")
print(f"There are {numbers} numeric strings.")
print(f"The sum of all the numbers {sum_numbers}")

print("-" * 40)
print("LEN|  OCCURRENCES  |NR.")
print("-" * 40)

for length in sorted(lengths):
    print(f"{length:>3}|{'*' * lengths[length]:<15}|{lengths[length]}")