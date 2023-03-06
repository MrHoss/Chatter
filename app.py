from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from nltk.chat.util import Chat, reflections
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import os

# Cria o chatbot
chatbot = ChatBot('Solubot')
r = sr.Recognizer()
mic = sr.Microphone()

# Treina o chatbot usando a biblioteca NLTK
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.portuguese')

dialogues = [
                'Qual seu nome?',
                'Meu nome é Solubot'
            ]

trainer = ListTrainer(chatbot)
trainer.train(dialogues)


# Define as regras de diálogo para o NLTK
rules = [
    (r'Oi|Olá|E aí', ['Olá!', 'E aí?', 'Oi!']),
    (r'Qual é seu nome', ['Meu nome é Solubot', 'Eu sou o Solubot seu amiguinho', 'Sou o Solubot, prazer!']),
    (r'Qual é a previsão do tempo para amanhã', ['Amanhã deve ser quente e ensolarado!', 'Amanhã pode ser quente e abafado!', 'Amanhã vai ser um dia quente!']),
    (r'(.*)clima(.*)', ['O clima parece estar quente e abafado nos próximos dias!', 'O clima está quente e úmido!', 'O clima está quente e seco!']),
    (r'bye|tchau|até logo|até a próxima', ['Até a próxima!', 'Tchau!', 'Até logo!']),
    (r'(.*)boleto(.*)|(.*)pagamento(.*)', ['Ok vou encaminhar a conversa para o setor financeiro!', 'aGUARDE, VOU TRANSFERIR PARA O FINANCEIRO!', 'Ok, você solicitou informações sobre boletos, ou encaminhar para o financeiro!']),
]
# Cria o chatbot para o NLTK
nltk_chatbot = Chat(rules, reflections)

def VoiceSinth(response):
    print("Bot: ", response)
    tts = gTTS(text=response, lang='pt-br')
    tts.save("response.mp3")
    playsound("response.mp3")

with mic as source:
    r.adjust_for_ambient_noise(source)  # ajusta o nível de ruído do ambiente
    while True:
        # Obtém a entrada de voz do usuário
        print('Estou escutando...')
        audio = r.listen(source)

        try:
            # Converte a entrada de voz em texto
            user_input = r.recognize_google(audio, language='pt-BR')
            print("Você: ", user_input)

            # Obtém a resposta do chatbot
            response = nltk_chatbot.respond(user_input)

            if not response:
                response = chatbot.get_response(user_input)
                if response.confidence < 0.5:
                    response = "Desculpe, eu não tenho certeza sobre a resposta."
                    VoiceSinth(response)
                else:
                    VoiceSinth(response.text)
            else:
                VoiceSinth(response)
            
        except sr.UnknownValueError:
            # Se não foi possível reconhecer o que foi dito, exibe uma mensagem de erro
            print("Desculpe, não entendi o que você disse.")
        except sr.RequestError as e:
            # Se houve um erro ao se comunicar com o servidor de reconhecimento de voz, exibe uma mensagem de erro
            print("Não foi possível se comunicar com o servidor de reconhecimento de voz. Erro: ", e)
