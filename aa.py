import random

def welcome():
    print("Welcome to the CSE Department Chat Bot!")
    print("How can I help you today?")

def respond_to_greeting():
    greetings = ["Hi!", "Hello!", "Hey there!"]
    return random.choice(greetings)

def get_user_input():
    return input("You: ")

def respond_to_user_input(user_input):
    if "courses" in user_input:
        return "We offer a variety of courses in computer science and engineering. You can check the course catalog for more details."
    elif "faculty" in user_input:
        return "Our faculty members are highly experienced and knowledgeable. You can find more information about them on our department website."
    elif "research" in user_input:
        return "Our department is actively involved in cutting-edge research in various areas of computer science and engineering. You can explore our research projects on the website."
    elif "help" in user_input:
        return "Feel free to ask me anything related to the CSE department, such as courses, faculty, research, etc."
    elif "goodbye" in user_input or "bye" in user_input:
        return "Goodbye! If you have more questions in the future, feel free to ask."
    else:
        return "I'm sorry, I didn't understand. Can you please rephrase or ask a different question?"

def main():
    welcome()

    while True:
        user_input = get_user_input()
        
        if user_input.lower() == 'exit':
            print("Goodbye! Have a great day!")
            break

        bot_response = respond_to_user_input(user_input)
        print("Bot:", bot_response)

if __name__ == "__main__":
    main()

