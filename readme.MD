# openai-dynamic-functions

This repo demonstrates dynamic function calling using OpenAI GPT API.

## Credits

https://github.com/Coding-Crashkurse/OpenAI-Function-Calling/tree/main

## Setup

- Fill .env with your OpenAI API key

```bash
pip install -r requirements.txt
python main.py
```

### Output

```
user query: I want to order one pizza Margherita to 124 Fakestreet
function call, name:  place_order , Arguments:  {'pizza_name': 'Margherita', 'quantity': 1, 'address': '124 Fakestreet'}
function response: Order placed successfully! Your order ID is 1. Total price is $12.0.
extra_info: {'total_orders': 12.0, 'last_order_id': 1, 'customer_address': '124 Fakestreet'}
AI response: Your order ID is 1. The total value is $12.0.

orders after 1st query : [{'order_id': 1, 'pizza_name': 'Margherita', 'quantity': 1, 'address': '124 Fakestreet', 'total_price': 12.0}]

user query: Please cancel this order and I want to order two pizza hawaii
function call, name:  cancel_order , Arguments:  {'order_id': 1}
function response: Order 1 has been canceled.
extra_info: {'total_orders': 0.0, 'last_order_id': None, 'customer_address': '124 Fakestreet'}
function call, name:  place_order , Arguments:  {'pizza_name': 'Hawaii', 'quantity': 2, 'address': '124 Fakestreet'}
function response: Order placed successfully! Your order ID is 2. Total price is $30.0.
extra_info: {'total_orders': 30.0, 'last_order_id': 2, 'customer_address': '124 Fakestreet'}
AI response: Your order for two pizzas Hawaii has been successfully placed. The total value of the order is $30.00, and the order ID is 2.

orders after 2nd query: [{'order_id': 2, 'pizza_name': 'Hawaii', 'quantity': 2, 'address': '124 Fakestreet', 'total_price': 30.0}]
```
