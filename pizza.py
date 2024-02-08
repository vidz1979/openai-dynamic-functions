database = {
    "pizzas": {"Hawaii": {"name": "Hawaii", "price": 15.0}, "Margherita": {"name": "Margherita", "price": 12.0}},
    "orders": [],
    "next_order_id": 1,
}


def place_order(pizza_name, quantity, address):
    if pizza_name not in database["pizzas"]:
        return f"We don't have {pizza_name} pizza!"

    if quantity < 1:
        return "You must order at least one pizza."

    order_id = database["next_order_id"]
    database["next_order_id"] += 1

    order = {
        "order_id": order_id,
        "pizza_name": pizza_name,
        "quantity": quantity,
        "address": address,
        "total_price": database["pizzas"][pizza_name]["price"] * quantity,
    }

    database["orders"].append(order)

    return f"Order placed successfully! Your order ID is {order_id}. Total price is ${order['total_price']}."


def get_pizza_info(pizza_name):
    if pizza_name in database["pizzas"]:
        pizza = database["pizzas"][pizza_name]
        return f"Pizza: {pizza['name']}, Price: ${pizza['price']}"
    else:
        return f"We don't have information about {pizza_name} pizza."


def cancel_order(order_id):
    for order in database["orders"]:
        if order["order_id"] == order_id:
            database["orders"].remove(order)
            return f"Order {order_id} has been canceled."
    return f"Order {order_id} not found."


functions = {
    "place_order": {
        "function": place_order,
        "definition": {
            "name": "get_pizza_info",
            "description": "Get name and price of a pizza of the restaurant",
            "parameters": {
                "type": "object",
                "properties": {
                    "pizza_name": {
                        "type": "string",
                        "description": "The name of the pizza, e.g. Hawaii",
                    },
                },
                "required": ["pizza_name"],
            },
        },
    },
    "get_pizza_info": {
        "function": get_pizza_info,
        "definition": {
            "name": "place_order",
            "description": "Place an order for a pizza from the restaurant",
            "parameters": {
                "type": "object",
                "properties": {
                    "pizza_name": {
                        "type": "string",
                        "description": "The name of the pizza you want to order, e.g. Margherita",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of pizzas you want to order",
                        "minimum": 1,
                    },
                    "address": {
                        "type": "string",
                        "description": "The address where the pizza should be delivered",
                    },
                },
                "required": ["pizza_name", "quantity", "address"],
            },
        },
    },
    "cancel_order": {
        "function": cancel_order,
        "definition": {
            "name": "cancel_order",
            "description": "Cancel an order from the restaurant",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The ID of the order you want to cancel",
                    },
                },
                "required": ["order_id"],
            },
        },
    },
}
