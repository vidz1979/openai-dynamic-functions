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
user: 'I want to order one pizza Margherita to 124 Fakestreet'
assistant:  tool_calls=[{'id': 'call_whBCjGOo029Jc1iCJSs1deJC', 'function': {'arguments': '{"pizza_name":"Margherita","quantity":1,"address":"124 Fakestreet"}', 'name': 'place_order'}, 'type': 'function'}]
extra_info: {'total_orders': 12.0, 'last_order_id': 1, 'customer_address': '124 Fakestreet'}
tool: 'Order placed successfully! Your order ID is 1. Total price is $12.0.' tool_call_id=call_whBCjGOo029Jc1iCJSs1deJC
assistant: 'Your order for one Margherita pizza has been placed with ID 1. The total price is $12.00.'

orders after 1st query : [{'order_id': 1, 'pizza_name': 'Margherita', 'quantity': 1, 'address': '124 Fakestreet', 'total_price': 12.0}]

user: 'Please cancel this order and I want to order two pizza hawaii'
assistant:  tool_calls=[{'id': 'call_kSph4nAOefPbMEYKPiQYpAOv', 'function': {'arguments': '{"order_id": 1}', 'name': 'cancel_order'}, 'type': 'function'}, {'id': 'call_hHDnhEdYSlcbXRJhAOmihmAt', 'function': {'arguments': '{"pizza_name": "Hawaii", "quantity": 2, "address": "124 Fakestreet"}', 'name': 'place_order'}, 'type': 'function'}]
extra_info: {'total_orders': 0.0, 'last_order_id': None, 'customer_address': '124 Fakestreet'}
tool: 'Order 1 has been canceled.' tool_call_id=call_kSph4nAOefPbMEYKPiQYpAOv
extra_info: {'total_orders': 30.0, 'last_order_id': 2, 'customer_address': '124 Fakestreet'}
tool: 'Order placed successfully! Your order ID is 2. Total price is $30.0.' tool_call_id=call_hHDnhEdYSlcbXRJhAOmihmAt
assistant: 'Your order for the Margherita pizza has been canceled. Your new order for two Hawaii pizzas has been placed with ID 2. The total price is $30.00.'

orders after 2nd query: [{'order_id': 2, 'pizza_name': 'Hawaii', 'quantity': 2, 'address': '124 Fakestreet', 'total_price': 30.0}]
```
