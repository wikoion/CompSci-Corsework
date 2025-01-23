def isPalindrome(word: str) -> bool:
    if len(word) <= 1:
        return True

    if word[0] != word[-1]:
        return False

    return isPalindrome(word[1:-1])

if __name__ == "__main__":
    word = input("Enter word: ")
    if isPalindrome(word):
        print(f"'{word}' is a palindrome")
    else: print(f"'{word}' is not a palindrome")
