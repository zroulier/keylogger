import json
from collections import defaultdict

def count_words_in_text(text, json_file):
    # Load the words from words.json
    with open(json_file, 'r') as file:
        words_list = json.load(file)

    # Initialize a dictionary to count word occurrences
    word_count = defaultdict(int)

    # Convert the text to lowercase for case-insensitive matching
    text = text.lower()

    # Search for each word in the text, allowing for matches within strings
    for word in words_list:
        word = word.lower()  # Ensure the word from words.json is also in lowercase
        # Use the count method to find how many times the word occurs in the text
        word_count[word] = text.count(word)

    return dict(word_count)

def read_text_from_file(text_file):
    # Read the content of text.txt
    with open(text_file, 'r') as file:
        return file.read()

# Example usage
if __name__ == "__main__":
    # Path to the text file
    text_file = 'text.txt'

    # Path to words.json
    json_file = 'words.json'

    # Read the content of text.txt
    text = read_text_from_file(text_file)

    # Call the function and get the word count
    word_count_result = count_words_in_text(text, json_file)

    # Print the word counts
    for word, count in word_count_result.items():
        print(f"'{word}': {count}")
