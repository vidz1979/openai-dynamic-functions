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
        self.func_definitions = [functions[function_name]["definition"] for function_name in functions]
        self.tools_defs = [
            {"type": "function", "function": functions[function_name]["definition"]} for function_name in functions
        ]
        self.functions = {function_name: function["function"] for function_name, function in functions.items()}
        self.prompt = {"role": "system", "content": prompt}
        self.messages: list[dict] = history if history else []
        self.model = model
        self.verbose = verbose
        self.extra_info = extra_info

    def chat(self, query):
        self.append_message({"role": "user", "content": query})
        return self.make_openai_request()

    def make_openai_request(self) -> str | None:
        response = openai.chat.completions.create(
            model=self.model,
            messages=[self.prompt, *self.messages] if self.prompt else self.messages,
            tools=self.tools_defs,
        )
        assistant_message = response.choices[0].message

        # Append the plain assistant message to the messages list
        self.append_message(assistant_message.model_dump(exclude_none=True))

        # If the assistant message contains tool calls, call the tools and make another request
        if assistant_message.tool_calls and len(assistant_message.tool_calls) > 0:
            # TODO parallel calls
            for tool_call in assistant_message.tool_calls:
                if tool_call.type == "function":
                    self.append_message(
                        {
                            "role": "tool",
                            "content": self.make_function_call(tool_call.function),
                            "tool_call_id": tool_call.id,
                        }
                    )
                else:
                    raise ValueError("Unknown tool call type")
            # Make another request with the function response
            return self.make_openai_request()
        else:
            # Message from AI is final, return the content
            return assistant_message.content

    def append_message(self, message):
        if self.verbose:
            print(
                message["role"] + ":",
                ("'" + message["content"] + "'") if "content" in message else "",
                ", ".join([f"{k}={v}" for k, v in message.items() if k not in ["role", "content"]]),
            )
        self.messages.append(message)

    def make_function_call(self, function_call):
        function_name = function_call.name
        arguments = json.loads(function_call.arguments)

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

        if self.verbose and self.extra_info:
            print("extra_info:", self.extra_info)

        return function_response
