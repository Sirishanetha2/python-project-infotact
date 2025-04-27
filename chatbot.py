from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def create_chatbot():
    chatbot = ChatBot('RecruitmentBot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")
    return chatbot

def chat_with_bot(chatbot, user_input):
    return chatbot.get_response(user_input)
