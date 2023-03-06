from chatterbot import ChatBot , filters
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from src.database.connect import pessoas

bot = ChatBot('Solubot',filters=[filters.get_recent_repeated_responses])
dialog=[]
trainer = ListTrainer(bot)
trainer.train(dialog)
#trainer.train(conversation2)
"""
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.portuguese.greetings")
trainer.train("chatterbot.corpus.portuguese.greetings")"""


while True:
    user_input = input("Você: ")
    bot_response = bot.get_response(user_input)
    print('Bot: ', bot_response)

""""app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug=True)"""