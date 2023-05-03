
from collections import Counter


def most_popular_characters(text):
    """

    :param text: text input from the user
    :return: popular characters ordered, to use for assigning hex values
    """
    popular_characters = Counter(text).most_common()
    return popular_characters


def create_hex_values(popular_characters):
    """
    creates hex values at the required length and format
    :param popular_characters: used to calculate the number of hex value sets required (f0, ff0 etc.)
    :return: hex values to use for assigning
    """
    hex_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e']
    sets = round((len(popular_characters)) / 14)
    for i in range(1, sets):
        new_set = ['f' * i + char for char in hex_values]
        hex_values += new_set
    return hex_values


def save_key(popular_characters):
    """

    :param popular_characters: for order of characters
    :return: nothing - creates key.txt file
    """
    with open('key.txt', 'w') as key_file:
        for tple in popular_characters:
            key_file.write(tple[0])

def load_key():
    """
    loads key.txt file created by save_key()
    :return: key
    """
    with open('key.txt', 'r') as key_file:
        key = key_file.readlines()[0]
    return key



def assign_hex_values(popular_characters, hex_values):
    """

    :param popular_characters: popular character order returned from most_popular_characters()
    :param hex_values: hex values created by create_hex_values()
    :return: assigned hex value tuple in form of (character, hex value)
    """
    assigned_hex_values = []
    for indx, char in enumerate(popular_characters):
        encryption_tuple = (char[0], hex_values[indx])
        assigned_hex_values.append(encryption_tuple)
    return assigned_hex_values

def assign_hex_values_key(key, hex_values):
    """

    :param key: loaded key file
    :param hex_values: hex values created by create_hex_values()
    :return: assigned hex values in tuple form of (character, hex value)
    """
    assigned_hex_values_key = []
    for indx, char in enumerate(key):
        encryption_tuple = (char, hex_values[indx])
        assigned_hex_values_key.append(encryption_tuple)
    return assigned_hex_values_key

def encrypt(text, character_hex_tuples):
    """
    :param text: Text to encrypt
    :param character_hex_tuples: Tuple of (character, hex) to encrypt with
    :returns: encrypted text
    """
    encrypted = ''
    for char in text:
        for tple in character_hex_tuples:
            if char == tple[0]:
                encrypted += tple[1]
    return encrypted

def decrypt(encrypted_text, character_hex_tuples):
    """

    :param encrypted_text: encrypted text in format
    :param character_hex_tuples: key to decryption - characters assigned to hex
    :return: decrypted text
    """
    decrypted = ''
    stored_hex = ''
    for indx, curr_hex in enumerate(encrypted_text):
        if curr_hex == 'f':
            stored_hex += curr_hex
        else:
            if len(stored_hex) > 0:
                # add current hex to stored hex if stored hex exists
                stored_hex += curr_hex
                # iterate over character_hex tuples to find character that belongs to stored hex
                for tple in character_hex_tuples:
                    if tple[1] == stored_hex:
                        decrypted += tple[0]
                        # reset stored hex after decrypting
                        stored_hex = ''
            else:
                # if not current hex is not 'f', and stored hex = 0 decrypt current hex
                for tple in character_hex_tuples:
                    if tple[1] == curr_hex:
                        decrypted += tple[0]
    return decrypted


def choose_option():
    """
    Take option choice - to except value errors
    :return: choice (int)
    """
    while True:
        try:
            choice = int(input('[1] Encrypt and create key\n[2] Decrypt with text\n[3] Decrypt with key (input 1, 2, 3 or 0 to exit): '))
            return choice
        except ValueError:
            print('Please enter a number [1], [2] or [3]. [0] to exit')

def main_menu():
    while True:
        choice = choose_option()

        if choice == 1:
            text = input('Please input text:\n ')
            popular_characters = most_popular_characters(text)
            save_key(popular_characters)
            hex_values = create_hex_values(popular_characters)
            character_hex_tuples = assign_hex_values(popular_characters, hex_values)
            encrypted = encrypt(text, character_hex_tuples)
            print(encrypted)

        elif choice == 2:
            encrypted_hex = input('Please input encrypted text:\n ')
            text = input('Please original input text (for character ordering):\n ')
            popular_characters = most_popular_characters(text)
            hex_values = create_hex_values(popular_characters)
            character_hex_tuples = assign_hex_values(popular_characters, hex_values)
            decrypted = decrypt(encrypted_hex, character_hex_tuples)
            print(f'Decrypted equal text? {decrypted==text}')
            print(decrypted)

        elif choice == 3:
            encrypted_hex = input('Please input encrypted text:\n ')
            key = load_key()
            hex_values = create_hex_values(key)
            character_hex_tuples = assign_hex_values_key(key, hex_values)
            decrypted = decrypt(encrypted_hex, character_hex_tuples)
            print(decrypted)

        elif choice == 0:
            break
        else:
            print('Error: Invalid choice')


if __name__ == '__main__':
    main_menu()