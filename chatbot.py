import inspect
import json
from typing import Any
import openai


class ChatBot:

    def __init__(
        self,
        functions: dict[str, dict[str, Any]],
        prompt: str = None,
        history: list[dict[str, str]] = None,
        model: str = "gpt-3.5-turbo-1106",
        verbose: bool = False,
        extra_info: dict[str, Any] = None,
    ):
        if history and prompt:
            raise ValueError("prompt and history cannot be used together")
        self.func_definitions = [functions[function_name]["definition"] for function_name in functions]
        self.functions = {function_name: function["function"] for function_name, function in functions.items()}
        self.messages = [{"role": "system", "content": prompt}] if prompt else []
        self.messages += history if history else []
        self.model = model
        self.verbose = verbose
        self.extra_info = extra_info

    def chat(self, query):
        if self.verbose:
            print("user query:", query)
        self.messages += [{"role": "user", "content": query}]
        return self.make_openai_request()

    def make_openai_request(self) -> str | None:
        response = openai.chat.completions.create(
            model=self.model,
            messages=self.messages,
            functions=self.func_definitions,
        )
        message = response.choices[0].message

        # If the message is a function call, call the function and make another request
        if message.function_call:
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)
            if self.verbose:
                print("function call, name: ", function_name, ", Arguments: ", arguments)

            # If the function has extra_info as an argument, add it to the function call
            if "extra_info" in inspect.getfullargspec(self.functions[function_name]).args and self.extra_info:
                arguments["extra_info"] = self.extra_info
            function_response = self.functions[function_name](**arguments)

            # If the function returns a tuple, the second element is extra_info
            if type(function_response) == tuple:
                function_response, extra_info = function_response
                if extra_info:
                    if self.extra_info:
                        self.extra_info.update(extra_info)
                    else:
                        self.extra_info = extra_info

            if self.verbose:
                print("function response:", function_response)
                if self.extra_info:
                    print("extra_info:", self.extra_info)

            # Add the function response to the messages and make another request
            self.messages += [
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            ]
            return self.make_openai_request()
        else:
            # Final message from the AI
            if self.verbose:
                print("AI response:", message.content)
            return message.content
