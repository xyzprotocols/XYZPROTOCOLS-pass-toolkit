import re
import sys
import os
import random
import hashlib
import requests
import time

# Colorama for colored terminal text
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("Colorama not found! Install it using: pip install colorama")
    sys.exit()

# ---------- CLEAR SCREEN ----------
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ---------- FANCY BANNER ----------
def print_banner():
    clear_screen()
    print(Fore.CYAN + """
    ╔══════════════════════════════════════════╗
          XYZ PROTOCOLS PASSWORD TOOLKIT
          Developed by xyzprotocols
          Version 1.3 - 2025
    ╚══════════════════════════════════════════╝
    """)

# ---------- LOADING EFFECT ----------
def loading_message(msg="Processing"):
    for i in range(3):
        print(Fore.CYAN + f"{msg}" + "." * (i + 1), end="\r")
        time.sleep(0.4)
    print(" " * 30, end="\r")  # Clear line

# ---------- EXIT ANIMATION ----------
def shutdown_animation():
    clear_screen()
    steps = [
        (Fore.CYAN, "[INFO] Saving logs..."),
        (Fore.CYAN, "[INFO] Encrypting session data..."),
        (Fore.CYAN, "[INFO] Closing network sockets..."),
        (Fore.YELLOW, "[WARNING] Clearing temporary files..."),
        (Fore.GREEN, "[DONE] Shutdown complete. Stay secure! 💻🔒")
    ]

    print(Fore.CYAN + "System shutting down...\n")
    for color, message in steps:
        print(color + message)
        time.sleep(0.8)

    print("\n" + Fore.CYAN + "Goodbye.\n")
    time.sleep(1.2)

# ---------- PASSWORD STRENGTH CHECKER ----------
def check_password_strength(password):
    score = 0
    tips = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        tips.append("Make your password at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        tips.append("Add uppercase letters (A-Z).")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("Add lowercase letters (a-z).")

    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("Include some numbers (0-9).")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        tips.append("Use special characters like !@#$%^&*")

    if score <= 2:
        strength = Fore.RED + "Weak ❌"
    elif 3 <= score <= 4:
        strength = Fore.YELLOW + "Medium ⚠️"
    else:
        strength = Fore.GREEN + "Strong ✅"

    return strength, tips

def strength_menu():
    print_banner()
    password = input(Fore.WHITE + "Enter your password: ")

    loading_message("Analyzing password")

    strength, tips = check_password_strength(password)

    print(Fore.CYAN + "\n══════════════════════════════════════════════")
    print(Fore.WHITE + f"Password Strength: {strength}")
    print(Fore.CYAN + "══════════════════════════════════════════════")

    if tips:
        print(Fore.YELLOW + "\nSuggestions to improve your password:")
        for tip in tips:
            print(Fore.WHITE + f"  - {tip}")
    else:
        print(Fore.GREEN + "\nYour password is strong! 💪")

# ---------- PASSWORD GENERATOR ----------
def generate_password(length=12, include_upper=True, include_lower=True, include_digits=True, include_symbols=True):
    chars = ""
    if include_upper:
        chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_lower:
        chars += "abcdefghijklmnopqrstuvwxyz"
    if include_digits:
        chars += "0123456789"
    if include_symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?"

    return ''.join(random.choice(chars) for _ in range(length)) if chars else None

def generator_menu():
    print_banner()
    try:
        length = int(input("Enter desired password length (e.g., 12): "))
    except ValueError:
        print(Fore.RED + "Invalid input! Using default length of 12.")
        length = 12

    print("\nSelect character types:")
    upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    digits = input("Include digits? (y/n): ").lower() == 'y'
    symbols = input("Include symbols? (y/n): ").lower() == 'y'

    loading_message("Generating secure password")

    password = generate_password(length, upper, lower, digits, symbols)
    if password:
        print(Fore.GREEN + "\nGenerated Password: " + Fore.WHITE + password)
        print(Fore.YELLOW + "Tip: Save it securely, don’t just screenshot it! 🔐")
    else:
        print(Fore.RED + "\nError: No character sets selected!")

# ---------- BREACH CHECK ----------
def breach_check(password):
    try:
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        first5, tail = sha1[:5], sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{first5}"

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None

        hashes = (line.split(':') for line in res.text.splitlines())
        for h, count in hashes:
            if h == tail:
                return int(count)
        return 0
    except:
        return None

def breach_menu():
    print_banner()
    password = input(Fore.WHITE + "Enter password to check: ")

    loading_message("Checking breaches")

    count = breach_check(password)
    if count is None:
        print(Fore.RED + "Error: Could not check password right now. Try again later.")
    elif count > 0:
        print(Fore.RED + f"⚠️ ALERT: This password was found {count} times in data breaches!")
        print(Fore.YELLOW + "Immediately stop using this password everywhere!")
    else:
        print(Fore.GREEN + "✅ Good news: This password was not found in known breaches.")

# ---------- MAIN MENU ----------
def main():
    while True:
        print_banner()
        print(Fore.WHITE + "1. Check password strength")
        print("2. Generate a secure password")
        print("3. Check if password is breached")
        print("4. Exit")
        print(Fore.CYAN + "══════════════════════════════════════════════")

        choice = input(Fore.CYAN + "Choose an option (1-4): ")

        if choice == '1':
            strength_menu()
        elif choice == '2':
            generator_menu()
        elif choice == '3':
            breach_menu()
        elif choice == '4':
            shutdown_animation()
            break
        else:
            print(Fore.RED + "\nInvalid choice! Please try again.")

        input(Fore.WHITE + "\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
