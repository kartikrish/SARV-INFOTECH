def simple_chatbot(user_input):

    #A simple rule-based chatbot function that responds to user input.
    
    # Convert input to lowercase to make the matching case-insensitive
    processed_input = user_input.lower()

    # Rule 1: Greeting
    if any(word in processed_input for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! How can I help you today? 😊"

    # Rule 2: Asking about the bot's identity/name
    elif any(word in processed_input for word in ["who are you", "what is your name"]):
        return "I am a simple rule-based chatbot built with Python. I don't have a name! 🤖"

    # Rule 3: Asking about the weather (simple keyword match)
    elif "weather" in processed_input:
        return "I can't check the current weather, but I hope it's a nice day where you are! ☀️"

    # Rule 4: Expressing thanks/gratitude
    elif any(word in processed_input for word in ["thank", "thanks", "tks", "cheers"]):
        return "You're welcome! Happy to assist. 👍"

    # Rule 5: Inquiry about services/capabilities
    elif any(word in processed_input for word in ["can you do", "help me"]):
        return "I can respond to basic greetings, identity questions, and simple keywords based on my rules."

    # Rule 6: Farewell/Goodbye
    elif any(word in processed_input for word in ["bye", "goodbye", "later", "cya"]):
        return "Goodbye! Have a great day! 👋"

    # Default/Catch-all Rule
    else:
        return "I'm sorry, I didn't understand that. Could you try rephrasing? 💬"

# --- Conversation Loop ---

print("Chatbot: Hello! I am a simple rule-based chatbot. Type 'bye' to exit.")

while True:
    # Get user input
    user_query = input("You: ")

    # Check for exit command first
    if user_query.lower() in ["bye", "exit", "quit"]:
        print("Chatbot: Goodbye! 👋")
        break

    # Get the response from the chatbot function
    response = simple_chatbot(user_query)

    # Print the chatbot's response
    print(f"Chatbot: {response}")