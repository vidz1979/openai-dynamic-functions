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

- First user interaction:

```
user query: I want to order one pizza Margherita to 124 Fakestreet
function call, name:  place_order , Arguments:  {'pizza_name': 'Margherita', 'quantity': 1, 'address': '124 Fakestreet'}
function response: Order placed successfully! Your order ID is 1. Total price is $12.0.
AI response: Your order for one Margherita pizza to 124 Fakestreet has been placed successfully. The total price is $12.0, and your order ID is 1.
```

Order is placed correctly:

```
orders: [{'order_id': 1, 'pizza_name': 'Margherita', 'quantity': 1, 'address': '124 Fakestreet', 'total_price': 12.0}]
```

- Second user interaction:

```
user query: Please cancel this order and I want to order two pizza hawaii
function call, name:  cancel_order , Arguments:  {'order_id': 1}
function response: Order 1 has been canceled.
function call, name:  place_order , Arguments:  {'pizza_name': 'Hawaii', 'quantity': 2, 'address': '124 Fakestreet'}
function response: Order placed successfully! Your order ID is 2. Total price is $30.0.
AI response: Your order for two Hawaiian pizzas has been placed successfully. The total value of the order is $30.0, and the order ID is 2.
```

Two functions were called successfully: cancel_order and place_order

```
orders: [{'order_id': 2, 'pizza_name': 'Hawaii', 'quantity': 2, 'address': '124 Fakestreet', 'total_price': 30.0}]
```
