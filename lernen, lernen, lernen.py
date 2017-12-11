import random
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  0   |
      |
      |
     ===''', ''' 
  +---+
  0   |
  |   |
      |
     ===''', '''
  +---+
  0   |
 /|   |
      |
     ===''', '''
  +---+   
  0   |
 /|\  | 
      |
     ===''', ''' 
  +---+
  0   |
 /|\  |
 /    |
     ===''', '''
  +---+
  0   |
 /|\  |
 / \  |  
     ===''']
words = '''ant baboon badger bat bear beaver camel car clam cobra cougar coyote crow deer dog donkey duck eagle ferret
fox frog goar goose hawk lion lizard lama mole monkey moose mouse mule newt otter owl panda paarat pigeon python rabbit 
ram tar raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel
whale wolf wombat zebra'''.split()

def getRandomWord(wordList):
    # Diese Funktion gibt einen zufällig ausgewählten String aus der übergebenen Liste zurück.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): #Ersetzt Unterstriche durch die korrekt erratenen Buchstaben.
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # Zeigt das Wort mit Leerzeichnen zwischen den Buchstaben an.
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Gibt den eingegebenen Buchstaben zurück. Diese Funktion sorgt dafür, dass nur ein Buchstabe und nichts anderes
    # eingegben wird
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print ('You have already guessed that letter. Choose again')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():
    # Gibt True zurück, wenn der Spieler noch einmal spielen möchte, anderenfalls False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')
