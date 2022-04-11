##### Setting Up the File #####

import random
import json

words_file = open(r'Words.txt')
words_text = words_file.read().splitlines()
words_file.close()

##### Declaring Variables #####

new_word_list = []
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = list('bcdfghjklmnpqrstvwxyz')
consonants_guessed = []
vowels_guessed = []
word_results = ""

player_info = {'Player 1':{'Round 1 Bank':0, 'Round 2 Bank':0, 'Total':0}, 
    'Player 2':{'Round 1 Bank':0, 'Round 2 Bank':0, 'Total':0},
    'Player 3':{'Round 1 Bank':0, 'Round 2 Bank':0, 'Total':0}}

for word in words_text:
   if word.isalpha() == True:
       new_word_list.append(word)

wheel = {}
wheel_cash_segments = range(18)

for number in wheel_cash_segments[1:]:
    wheel[number] = 50 + (50 * number)

wheel[18] = 'Lose a Turn'
wheel[19] = 'bankrupt'.upper()

round_money = 0

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
    
    global round_money
    global consonant_guessed_correctly
    global word_guessed_correctly
    global consonants_guessed
    global word_results
    
    print(consonants_guessed)
    
    consonant_guess = input("Guess a consonant or guess a word").lower()
    
    if len(consonant_guess) == 1:
        if consonant_guess in consonants and consonant_guess not in consonants_guessed and consonant_guess.isalpha():
            consonants_guessed.append(consonant_guess)
            if consonant_guess in word_choice:
                round_money = round_money + (wheel[segment_number] * int(word_choice.count(consonant_guess)))
                for letter_spot in range(len(word_choice)):
                    if(word_choice[letter_spot] == consonant_guess):
                        listed_word[letter_spot] = word_choice[letter_spot]
                print("That letter is in there!")
                word_results = "".join(listed_word)
                print(word_results)
                return
        elif consonant_guess not in consonants:
            print("Please choose a consonant.")
            guess_consonant()

        elif consonant_guess not in word_choice:
            print("That's not in there")
            consonant_guessed_correctly = False
            return

    elif len(consonant_guess) > 1: 
        if consonant_guess.lower() == word_choice.lower():
            print("You did it!")
            word_guessed_correctly = True
            return
        else:
            print("That is not the word.")
            word_guessed_correctly = False
            return

def guess_vowel():
    
    global round_money
    global vowel_guessed_correctly
    global word_guessed_correctly
    global vowels_guessed
    global word_results
    
    print(vowels_guessed)
    print(word_results)
    
    if round_money < 250:
        print("Not enough money to buy a vowel.")
    vowel_choice = input("Buy a vowel for $250? Y/N or guess a word by typing W")
    print(f'Here are the vowels guessed so far: {vowels_guessed}')
    if vowel_choice.upper() == "Y":
        vowel_guess = input("Guess a vowel")
        if vowel_guess in vowels and vowel_guess not in vowels_guessed and vowel_guess.isalpha():
            round_money = round_money - 250
            vowels_guessed.append(vowel_guess)
            if vowel_guess in word_choice:
                round_money = round_money - 250
                for letter_spot in range(len(word_choice)):
                    if(list(word_choice[letter_spot]) == vowel_guess):
                        listed_word[letter_spot] = word_choice[letter_spot]
                print("That letter is in there!")
                word_results = "".join(listed_word)
                print(word_results)
                return
        elif vowel_guess not in vowels:
            print("Please choose a vowel")
            
        elif vowel_guess not in word_choice:
            print("That vowel is not in there")
            vowel_guessed_correctly = False

    elif vowel_choice.upper() == 'N':
        return
    elif vowel_choice.upper() == 'W':
        word_guess = input("Guess a word!")
        if word_guess.lower() == word_choice.lower():
                print("You did it!")
                word_guessed_correctly = True
                return
        else:
            print("That is not the word.")
            word_guessed_correctly = False
            return

choose_word()
word_choice = "Hello".lower()
segment_number = random.randint(1, 19)
round_money = 300
guess_vowel()
print(word_choice)
print(listed_word)
print(word_results)
print(round_money)
