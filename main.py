from openai import OpenAI
from chatbot import ChatBot
from dotenv import load_dotenv

load_dotenv()

from pizza import functions, database

client = OpenAI()

bot = ChatBot(
    prompt="You are a pizza restaurant chatbot. If a customer order a pizza, always inform total value and ID of the order.",
    functions=functions,
    verbose=True,
)

query = "I want to order one pizza Margherita to 124 Fakestreet"
response = bot.chat(query)
print("orders:", database["orders"])

query = "Please cancel this order and I want to order two pizza hawaii"
response = bot.chat(query)
print("orders:", database["orders"])
