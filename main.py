import openai
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

class ChattyMary:
    def __init__(self):
        self.bot = ChatBot(
            'ChattyMary',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///database.sqlite3'
        )
        self.setup_trainers()
        self.setup_openai()

    def setup_trainers(self):
        trainer = ChatterBotCorpusTrainer(self.bot)
        trainer = ListTrainer(self.bot)
        trainer.train([
            "What do I need to make a dirty vodka martini?",
            "Sounds like fun! You will need the following ingredients:\n 2.5 to 3 oz quality vodka\n0.5 oz dry vermouth (adjust to taste)\n0.5 to 1 oz olive brine (from a jar of green olives; use more for a 'dirtier' martini)\n IceGreen olives, for garnish",
        ])
        trainer.train("chatterbot.corpus.english")

    def setup_openai(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            print("Warning: OPENAI_API_KEY environment variable not set")

    def talk_to_gpt(self, prompt):
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=prompt
            )
            return response.choices[0].text
        except Exception as e:
            return f"Error communicating with GPT: {str(e)}"

    def chat(self):
        print("ChattyMary: Hello! I'm ready to chat. Press Ctrl+C to exit.")
        while True:
            try:
                user_input = input("You: ")
                bot_response = self.bot.get_response(user_input)
                print("Bot: ", bot_response)
            except (KeyboardInterrupt, EOFError, SystemExit):
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    chatty = ChattyMary()
    chatty.chat() 