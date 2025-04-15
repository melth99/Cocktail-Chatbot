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
            database_uri='sqlite:///database.sqlite3',
            COCKTAIL_BASE_URL="https://www.thecocktaildb.com/api/json/v1/",
            COCKTAIL_API_KEY=os.getenv("COCKTAIL_API_KEY"),
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
        )
        self.setup_trainers()
        self.setup_openai()
       

    def setup_trainers(self):
        trainer = ChatterBotCorpusTrainer(self.bot)
        trainer.train("chatterbot.corpus.english")
        trainer.train("chatterbot.corpus.english.greetings")
        trainer.train("chatterbot.corpus.english.conversations")
        trainer.train("chatterbot.corpus.english.food")
        trainer.train("chatterbot.corpus.english.science")
        trainer.train("chatterbot.corpus.english.humor")
        trainer.train("chatterbot.corpus.english.emotion")
        trainer.train([
            "Hi I'm Chatty Mary! What kind of drinks do you want help with?",
            "What do I need to make a dirty vodka martini?",
            "Sounds like fun! You will need the following ingredients:\n 2.5 to 3 oz quality vodka\n0.5 oz dry vermouth (adjust to taste)\n0.5 to 1 oz olive brine (from a jar of green olives; use more for a 'dirtier' martini)\n IceGreen olives, for garnish",
            "What is the best way to make a dirty vodka martini?",
            "To make a dirty vodka martini, you will need to follow these steps:\n1. Pour 2.5 to 3 oz of quality vodka into a martini glass.\n2. Add 0.5 oz of dry vermouth (adjust to taste).\n3. Add 0.5 to 1 oz of olive brine (from a jar of green olives; use more for a 'dirtier' martini).\n4. Add ice to the glass.\n5. Add green olives for garnish.",
            "Does this drink have a lot of alcohol?",
            "Absolutely! A standard dirty martini typically has an alcohol content around 29% ABV (58 proof) after mixing and dilution with ice. This is much higher than most mixed drinks, beers, or wines."
        ])
    def setup_openai(self):
        if not self.OPENAI_API_KEY:
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
        
        
    def get_cocktail_data(self):
        if not self.COCKTAIL_API_KEY:
            print("Warning: COCKTAIL_API_KEY environment variable not set")

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
