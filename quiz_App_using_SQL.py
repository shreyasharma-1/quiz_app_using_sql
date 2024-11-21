import random
import mysql.connector
import os
import platform


def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shreya1104",
        database="quizApp"
    )


def load_questions(language):
    questions = []
    conn = connect_to_db()
    cur = conn.cursor()
    query = "SELECT question, option1, option2, option3, option4, correct_answer FROM questions WHERE language = %s"
    cur.execute(query, (language,))
    for row in cur.fetchall():
        question = row[0]
        options = [row[1], row[2], row[3], row[4]]
        correct_answer = row[5]
        questions.append((question, options, correct_answer))
    cur.close()
    conn.close()
    return questions


def save_score(username, score, language):
    conn = connect_to_db()
    cur = conn.cursor()
    query = "INSERT INTO scores (username, score, language) VALUES (%s, %s, %s)"
    cur.execute(query, (username, score, language))
    conn.commit()
    cur.close()
    conn.close()


def validate_password(password):
    if len(password) < 8 or len(password) > 12:
        print("Password must be between 8 and 12 characters long.")
        return False
    if not any(char in ["#", "$", "@", "&", "!"] for char in password):
        print("Password must contain at least one special character: #, $, @, &, !")
        return False
    if not any(char.isdigit() for char in password):
        print("Password should have at least one digit!")
        return False
    if not any(char.isupper() for char in password):
        print("Password should have at least one uppercase letter!")
        return False
    return True


def run_quiz(language, questions):
    score = 0
    random.shuffle(questions)
    selected_questions = questions[:5]
    for i, (question, options, correct_answer) in enumerate(selected_questions):
        print(f"\nQ{i+1}: {question}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        answer = input("Your answer (number or option): ").strip().lower()
        if answer == correct_answer or answer == options[int(correct_answer) - 1].lower():
            score += 1
            print("Correct!")
        else:
            print(f"Wrong! The correct answer is: {options[int(correct_answer) - 1]}")
    print(f"\nYou scored {score} out of 5.")
    return score


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def main():
    print("Welcome to the Quiz Game!")
    username = input("Enter your username: ")

    
    while True:
        password = input("Enter your password: ")
        if validate_password(password):
            print("Password is valid.")
            break

    while True:
        clear_screen()
        print("\nChoose a language for the quiz:")
        print("1/a. Python")
        print("2/b. Java")
        print("3/c. C++")
        choice = input("Enter the number of your choice: ")

        if choice == '1' or choice == "python" or choice == "PYTHON" or choice == "a":
            language = "Python"
        elif choice == '2' or choice == "java" or choice == "JAVA" or choice == "b":
            language = "Java"
        elif choice == '3' or choice == "c++" or choice == "C++" or choice == "c":
            language = "C++"
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        questions = load_questions(language)
        if not questions:
            print(f"No questions available for {language}.")
            continue

        score = run_quiz(language, questions)
        save_score(username, score, language)

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thank you for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
