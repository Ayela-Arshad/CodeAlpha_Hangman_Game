import random
import requests

def get_random_word():
    """
    Fetches a random word from an API and ensures it has a valid meaning.
    """
    while True:
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
            if response.status_code == 200:
                word = response.json()[0]
                if check_word_meaning(word):
                    return word.lower()
                else:
                    print(f"'{word}' does not have a valid meaning. Fetching another word...")
            else:
                print("Failed to fetch a word from the API, using a fallback word.")
                fallback_word = random.choice(["snake", "headache", "decorum", "javascript", "elephant", "computer", "programming", "software"])
                if check_word_meaning(fallback_word):
                    return fallback_word
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            fallback_word = random.choice(["snake", "headache", "decorum", "javascript", "elephant", "computer", "programming", "software"])
            if check_word_meaning(fallback_word):
                return fallback_word

def check_word_meaning(word):
    """
    Checks if the word has a valid meaning by querying the Dictionary API.
    """
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200 and response.json():
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking the meaning: {e}")
        return False

def get_word_meaning(word):
    """
    Fetches the meaning of the word from the Dictionary API.
    """
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            meanings = response.json()[0]['meanings']
            definition = meanings[0]['definitions'][0]['definition']
            return definition
        else:
            return "No definition found for the word."
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the meaning: {e}")
        return "No definition found due to an error."
