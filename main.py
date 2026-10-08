
import random


def generate_secret_number() -> str:
    """Generate a four-digit number with unique digits."""
    first_digit = random.choice("123456789")
    remaining_digits = [digit for digit in "0123456789"
                        if digit != first_digit]
    other_digits = random.sample(remaining_digits, 3)
    return first_digit + "".join(other_digits)


def print_intro() -> None:
    """Display the welcome message and game instructions."""
    print("Hi there!")
    print("-" * 40)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print("-" * 40)
    print("Enter a number:")
    print("-" * 40)


def validate_guess(guess: str) -> str:
    """Check whether the player's guess is valid."""
    if len(guess) != 4:
        return "Your number must contain exactly 4 digits."
    if not guess.isdigit():
        return "Your number must contain only digits."
    if guess[0] == "0":
        return "Your number must not start with zero."
    if len(set(guess)) != 4:
        return "Your number must not contain duplicate digits."
    return ""


def count_bulls_and_cows(
    secret: str, guess: str
) -> tuple[int, int]:
    """Count matching digits in correct and incorrect positions."""
    bulls = sum(
        secret[index] == guess[index]
        for index in range(4)
    )
    cows = sum(digit in secret for digit in guess) - bulls
    return bulls, cows


def format_result(count: int, singular: str, plural: str) -> str:
    """Return the correct singular or plural word."""
    word = singular if count == 1 else plural
    return f"{count} {word}"


def play_game() -> None:
    """Run the game until the secret number is guessed."""
    secret = generate_secret_number()
    attempts = 0
    print_intro()

    while True:
        guess = input(">>> ").strip()
        error = validate_guess(guess)

        if error:
            print(f"Invalid input: {error}")
            print("-" * 40)
            continue

        attempts += 1

        if guess == secret:
            print("Correct, you've guessed the right number")
            print(f"in {attempts} guesses!")
            print("-" * 40)
            print("That's amazing!")
            break

        bulls, cows = count_bulls_and_cows(secret, guess)
        bull_text = format_result(bulls, "bull", "bulls")
        cow_text = format_result(cows, "cow", "cows")
        print(f"{bull_text}, {cow_text}")
        print("-" * 40)


if __name__ == "__main__":
    play_game()
