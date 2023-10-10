import string
import random

def passGen(length, exChars):
    # filter excluded characters out of string.punctuation
    specialChars = ''.join(char for char in string.punctuation if char not in exChars)
    # create password string 
    while True:
        password = ''.join(
            random.choices(string.ascii_letters + string.digits + specialChars, 
            k=int(length)))
        # ensure excluded characters are not present in password
        if all(char not in exChars for char in password):
            return password
# get user input    
passwordLength = input("How long should the password be? ")
exclusions = input("Enter special characters to exclude: ")

print(passGen(passwordLength, exclusions))