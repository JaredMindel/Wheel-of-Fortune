##### NOTES/FUTURE FIXES #####

# Need to fix flow control; will need to scrap some stuff but I know what to do
# Plan to make the UI more intuitive and clear
# Going to fix some inputs, making them variables as opposed to simple inputs that only exist for 1 line

##### Setting Up the File #####

import random
from threading import Timer

words_file = open(r'Words.txt')
words_text = words_file.read().splitlines()
words_file.close()

##### Declaring Variables #####

new_word_list = []
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = list('bcdfghjklmnpqrstvwxyz')
consonants_guessed = []
vowels_guessed = []

player_info = {'Player 1':{'Round 1 Bank':0, 'Round 2 Bank':0, 'Total':0}, 
    'Player 2':{'Round 1 Bank':0, 'Round 2 Bank':0, 'Total':0},
    'Player 3':{'Round 1 Bank':0, 'Round 2 Bank':0, 'Total':0}}

print(player_info)

round_money = 0

for word in words_text:
   if word.isalpha() == True:
       new_word_list.append(word)

wheel = {}
wheel_cash_segments = range(18)

for number in wheel_cash_segments[1:]:
    wheel[number] = 50 + (50 * number)

wheel[18] = 'Lose a Turn'
wheel[19] = 'bankrupt'.upper()

##### Creating Functions #####

def bankrupt(player, round):
    print('Uh oh! You hit BANKRUPT')
    if player == 1:
        if round == 1:
            player_info['Player 1']['Round 1 Bank'] = 0
        elif round == 2:
            player_info['Player 1']['Round 2 Bank'] = 0
    elif player == 2: 
        if round == 1:
            player_info['Player 2']['Round 1 Bank'] = 0
        elif round == 2:
            player_info['Player 2']['Round 2 Bank'] = 0
    elif player == 3:
        if round == 1:
            player_info['Player 3']['Round 1 Bank'] = 0
        elif round == 2:
            player_info['Player 3']['Round 2 Bank'] = 0

def choose_word():
    global word_choice
    global number
    global listed_word
    listed_word = []
    word_choice = random.choice(new_word_list).lower()
    for number in word_choice:
        listed_word.append("_")

def guess_consonant():
    global guessed_correctly_value
    global consonant_guess
    print(consonants_guessed)
    consonant_guess = input("Guess a consonant or type a word to guess a word")
    if len(consonant_guess) == 1:
        if consonant_guess not in consonants and consonant_guess not in consonants_guessed and consonant_guess not in vowels:
            consonants_guessed.append(consonant_guess)
            print("That's not a consonant. Pick again.")
            guess_consonant()
        elif consonant_guess in consonants_guessed:
            print("Choose a different consonant.")
            guess_consonant()
    elif len(consonant_guess) > 1:
        if consonant_guess.lower() == word_choice.lower():
            print("You guessed correctly")
            guessed_correctly_value = 1
            return
        else:
            return

def buy_vowel():
    global all_vowels_guessed
    global round_money
    global vowels_guessed
    global vowel_chosen
    global vowel_not_in_word
    vowel_not_in_word = 0
    if len(vowels_guessed) == 5:
        all_vowels_guessed = 1
    else: 
        print(vowels_guessed)
        if round_money < 250:
            print("Oops! You don't have enough money.")
        else:
            print(f'Your current budget: ${round_money}')
            vowel_chosen = input("Buy a vowel for $250")
            if vowel_chosen not in vowels:
                print("That's not a vowel. Pick again.")
                buy_vowel()
            elif vowel_chosen in word_choice and vowel_chosen not in vowels_guessed and vowel_chosen not in consonants:
                vowels_guessed.append(vowel_chosen)
                for letter_spot in range(len(word_choice)):
                    if(word_choice[letter_spot] == vowel_chosen):
                        listed_word[letter_spot] = word_choice[letter_spot]
                print("".join(listed_word))
                if input("Would you like to guess a vowel? Y/N or W for word").upper() == "Y":
                    round_money = round_money - 250
                    buy_vowel()
                elif input("Would you like to guess a vowel? Y/N or W for word").upper() == "N":
                    return
            elif vowel_chosen in vowels_guessed:
                print("This vowel has already been chosen, chose another one.")
                buy_vowel()
            elif vowel_chosen not in word_choice: 
                print("That vowel is not in the word")
                if vowel_chosen not in vowels_guessed and vowel_chosen not in consonants:
                    vowels_guessed.append(vowel_chosen)

choose_word()

def set_bank(player, round, round_money):

    if player == 1:
        if round == 1:
            player_info['Player 1']['Round 1 Bank'] = round_money
        if round == 2:
            player_info['Player 1']['Round 2 Bank'] = round_money
    elif player == 2:
        if round == 1:
            player_info['Player 2']['Round 1 Bank'] = round_money
        if round == 2:
            player_info['Player 2']['Round 2 Bank'] = round_money
    elif player == 3:
        if round == 1:
            player_info['Player 3']['Round 1 Bank'] = round_money
        if round == 2:
            player_info['Player 3']['Round 2 Bank'] = round_money

def set_round_money(player, round):
    global round_money
    if player == 1:
        if round == 1:
            round_money = player_info['Player 1']['Round 1 Bank']
        if round == 2:
            round_money = player_info['Player 1']['Round 2 Bank']
    elif player == 2:
        if round == 1:
            round_money = player_info['Player 2']['Round 1 Bank']
        if round == 2:
            round_money = player_info['Player 2']['Round 2 Bank']
    elif player == 3:
        if round == 1:
            round_money = player_info['Player 3']['Round 1 Bank']
        if round == 2:
            round_money = player_info['Player 3']['Round 2 Bank']

player = 1
all_vowels_guessed = 0
def spin_wheel(player, round):

    global guessed_correctly_value
    guessed_correctly_value = 0
    global round_money
    print(word_choice)

    if "".join(listed_word).lower() == word_choice.lower():
        guessed_correctly_value = 1
        return None

    while guessed_correctly_value == 0:
        segment_number = random.randint(1, 19)

        set_round_money(player, round)

        print("".join(listed_word))

        if player == 1 or player == 2:
            next_player = int(player + 1)
        elif player == 3:
            next_player = 1
        
        print(f'Player: {player}, Round: {round}')

        print(f'You can earn: ${wheel[segment_number]}')
        print(f'Your current budget: ${round_money}')
        
        if wheel[segment_number] == 'Lose a Turn':
            spin_wheel(player = next_player, round = round)
        elif wheel[segment_number] == 'BANKRUPT':
            bankrupt(player, round)
            spin_wheel(next_player, round)
        elif wheel[segment_number] in range(100,950):
            guess_consonant()
            if consonant_guess.lower() == word_choice:
                guessed_correctly_value = 1
                break
            if "".join(listed_word).lower() == word_choice:
                guessed_correctly_value = 1
                break
            if consonant_guess in word_choice and consonant_guess not in consonants_guessed and consonant_guess not in vowels:
                consonants_guessed.append(consonant_guess)
                round_money = round_money + (wheel[segment_number] * word_choice.count(consonant_guess))
                set_bank(player, round, round_money)
                print(f'Your current budget: ${round_money}')
                for x in range(len(listed_word)):
                    if consonant_guess == word_choice[x]:
                        listed_word[x] = consonant_guess
                print("".join(listed_word))
                while len(vowels_guessed) < 5:
                    while round_money >= 250:
                        print(f'Current budget: ${round_money}')
                        if "".join(listed_word) == word_choice.lower():
                            guessed_correctly_value = 1
                            break
                        vowel_input = input("Would you like to buy a vowel? Y/N or W to guess a word.").upper()
                        if vowel_input == 'Y':
                            print("".join(listed_word))
                            buy_vowel() 
                            if vowel_chosen not in vowels_guessed and vowel_chosen not in consonants:
                                vowels_guessed.append(vowel_chosen)
                                if vowel_chosen not in word_choice:
                                    round_money = round_money - 250
                                    set_bank(player, round, round_money)
                                    spin_wheel(next_player, round)
                            else:
                                round_money = round_money - 250
                                for x in range(len(listed_word)):
                                    if vowel_chosen == word_choice[x]:
                                        listed_word[x] = vowel_chosen
                                if vowel_chosen not in word_choice:
                                    spin_wheel(next_player, round)
                                print("".join(listed_word))
                                continue
                        elif vowel_input == "N":
                            break
                        elif vowel_input == 'W':
                            word_guess = input("What's your guess?")
                            if word_guess.lower() == word_choice.lower():
                                print("You did it!")
                                guessed_correctly_value = 1
                                break
                            else:
                                print("Nope! Wrong word!")
                                spin_wheel(next_player, round)
                        elif guessed_correctly_value == 1:
                            break
                    spin_wheel(next_player, round)
                spin_wheel(player, round)
            else:
                if consonant_guess.lower() == word_choice.lower():
                    guessed_correctly_value = 1
                    return
                print("That consonant is not there")
                if consonant_guess not in vowels and consonant_guess.isalpha() and consonant_guess not in consonants_guessed:
                    consonants_guessed.append(consonant_guess)
                spin_wheel(next_player, round)
        while round_money >= 250:
            print(f'current budget: ${round_money}')
            vowel_input = input("Would you like to buy a vowel? Y/N or W for word").upper()
            if vowel_input == 'Y':
                print("".join(listed_word))
                buy_vowel() 
                if vowel_chosen not in vowels_guessed:
                    spin_wheel(next_player, round)
                round_money = round_money - 250
                set_bank(player, round, round_money)
                for x in range(len(listed_word)):
                    if vowel_chosen == word_choice[x]:
                        listed_word[x] = vowel_chosen
                print("".join(listed_word))
                continue
            elif vowel_input == "N":
                spin_wheel(player, round)
            elif vowel_input == 'W':
                word_guess = input("What's your guess?")
                if word_guess.lower() == word_choice.lower():
                    print("You did it!")
                    guessed_correctly_value = 1
                    break
                else:
                    print("Nope! Wrong word!")
                    spin_wheel(next_player, round)
            else: 
                print("You're out of money! Spin the wheel again.")
                break

##### Round 1 #####

spin_wheel(player = 1, round = 1)
print(f'The word was {word_choice}. Onto the next round.')
print(player_info)

##### Round 2 #####

listed_word = []
all_vowels_guessed = []
vowels_guessed = []
consonant_guessed = []
round_money = 0

choose_word()
spin_wheel(player = 1, round = 2)
print(f'The word was {word_choice}. Onto the next round.')

##### Determining the Winner #####

player_info['Player 1']['Total'] = player_info['Player 1']['Round 1 Bank'] + player_info['Player 1']['Round 2 Bank']
player_info['Player 2']['Total'] = player_info['Player 2']['Round 1 Bank'] + player_info['Player 2']['Round 2 Bank']
player_info['Player 3']['Total'] = player_info['Player 3']['Round 1 Bank'] + player_info['Player 3']['Round 2 Bank']

print(player_info)

advancing_player = ''

if (player_info['Player 1']['Total'] > player_info['Player 2']['Total']) and (
    player_info['Player 1']['Total'] > player_info['Player 3']['Total']):
        advancing_player = 1
elif (player_info['Player 2']['Total'] > player_info['Player 1']['Total']) and (
    player_info['Player 2']['Total'] > player_info['Player 3']['Total']):
        advancing_player = 2
elif (player_info['Player 3']['Total'] > player_info['Player 1']['Total']) and (
    player_info['Player 3']['Total'] > player_info['Player 2']['Total']):
        advancing_player = 3

print(f' The advancing player is Player {advancing_player}')

##### Final Round #####

listed_word = []
choose_word()
for x in range(len(word_choice)):
    if 'R'.lower() == word_choice[x]:
        listed_word[x] = 'r'
    if 'S'.lower() == word_choice[x]:
        listed_word[x] = 's'
    if 'T'.lower() == word_choice[x]:
        listed_word[x] = "t".lower()
    if 'l'.lower() == word_choice[x]:
        listed_word[x] = "l".lower()
    if 'n'.lower() == word_choice[x]:
        listed_word[x] = "n".lower()
    if 'e'.lower() == word_choice[x]:
        listed_word[x] = "e".lower()
print("".join(listed_word))
final_vowel = input("What vowel do you want?")
for x in range(len(word_choice)):
    if word_choice[x].lower() == final_vowel.lower():
        listed_word[x] = final_vowel.lower()
print("".join(listed_word))

timeout = 5

t = Timer(timeout, print, ["You ran out of time! You lose!"])
t.start()
prompt = (f'"You have %i seconds to guess the word Guess the word. Go!' % timeout)
final_input = input(prompt)
t.cancel()
if final_input.lower() == word_choice.lower():
    print("You got it right! You receive $6 million")
else:
    print("You lost!")