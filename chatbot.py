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
    ):
        if history and prompt:
            raise ValueError("prompt and history cannot be used together")
        self.func_definitions = [functions[function_name]["definition"] for function_name in functions]
        self.functions = {function_name: function["function"] for function_name, function in functions.items()}
        self.messages = [{"role": "system", "content": prompt}] if prompt else []
        self.messages += history if history else []
        self.model = model
        self.verbose = verbose

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

        if message.function_call:
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)
            if self.verbose:
                print("function call, name: ", function_name, ", Arguments: ", arguments)
            function_response = self.functions[function_name](**arguments)
            if self.verbose:
                print("function response:", function_response)

            self.messages += [
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            ]
            return self.make_openai_request()
        else:
            if self.verbose:
                print("AI response:", message.content)
            return message.content
