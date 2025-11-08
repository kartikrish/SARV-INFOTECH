import random
import datetime
import re
#import requests  # for API access later

class EcoChatBot:
    def __init__(self):
        self.mode = "normal"

        self.responses = {
            'greeting': r'\b(hi|hello|hey|yo|sup)\b',
            'mood': r'\b(how are you|how do you do)\b',
            'date': r'\b(date|today)\b',
            'time': r'\b(time|clock)\b',
            'calculator': r'\b(calculate|add|subtract|multiply|divide)\b',
            'bye': r'\b(bye|exit|quit|goodbye)\b'
        }

        print("🌿 EcoChatBot: Hello! I’m your eco-friendly smart assistant 🌱")
        print("I can chat naturally and help with simple tasks.")
       
    # --- MAIN RESPONSE FUNCTION ---
    def respond(self, user_input):
        user_input = user_input.lower()

        # Switch to advanced mode
        if "ved" in user_input:
            self.mode = "advanced"
            return "🌱 Switched to advanced mode! You can now ask me anything, or request notes/reports."

        # Exit
        if re.search(self.responses['bye'], user_input):
            return "🌿 Goodbye! Stay green and positive!"

        # Normal Mode
        if self.mode == "normal":
            return self.handle_normal_mode(user_input)
        else:
            return self.handle_advanced_mode(user_input)

    # --- NORMAL MODE HANDLING ---
    def handle_normal_mode(self, user_input):
        if re.search(self.responses['greeting'], user_input):
            return random.choice([
                "Hey there! 🌼",
                "Hello! How’s your day going?",
                "Hi! Ready to chat about something chill?"
            ])
        elif re.search(self.responses['mood'], user_input):
            return random.choice([
                "I'm feeling eco-happy today 🌿",
                "All systems green! How about you?",
                "Just enjoying the digital sunshine ☀️"
            ])
        elif re.search(self.responses['date'], user_input):
            return f"Today's date is {datetime.date.today()} 🌼"
        elif re.search(self.responses['time'], user_input):
            return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')} ⏰"
        elif re.search(self.responses['calculator'], user_input):
            return self.handle_calculator(user_input)
        else:
            return random.choice([
                "Hmm, interesting! Tell me more about that 🌿",
                "I’m not sure I get that — could you explain a bit more?",
                "Haha, that’s cool 😄 — you’ve got a fun vibe!"
            ])

    # --- ADVANCED MODE HANDLING ---
    def handle_advanced_mode(self, user_input):
        # Replace this with your API endpoint later
        if "note" in user_input:
            return "📝 Sure! Tell me what you’d like the note to say."
        elif "report" in user_input:
            return "📄 Okay! What should I write the report about?"
        else:
            return self.ask_api(user_input)

    # --- API CALL PLACEHOLDER ---
    def ask_api(self, query):
        """
        This is the function you’ll connect to an actual API later.
        Example: OpenAI, Gemini, local LLM, or any REST AI endpoint.
        """
        try:
            # Example (replace URL with your model endpoint):
            # response = requests.post("https://api.example.com/chat", json={"input": query})
            # return response.json()['answer']
            return f"(API Placeholder) You asked: '{query}'. In advanced mode, I’d get this from an AI API 🌍"
        except Exception as e:
            return f"⚠️ Sorry, I couldn’t reach the API. Error: {e}"

    # --- BASIC CALCULATOR ---
    def handle_calculator(self, user_input):
        try:
            expression = re.findall(r'[-+*/\d\s.]+', user_input)
            if expression:
                result = eval(expression[0])
                return f"The result is {result} 🌱"
            else:
                return "Please provide a valid calculation like 'calculate 5+3'."
        except:
            return "Sorry, I couldn’t calculate that. Try again."

# --- MAIN LOOP ---
ved = EcoChatBot()

while True:
    user_input = input("\nYou: ")
    response = ved.respond(user_input)
    print("Bot:", response)
    if "goodbye" in response.lower():
        break
