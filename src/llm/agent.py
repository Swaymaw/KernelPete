# %%

from litellm import completion

from src.utils.schema import ModelResult


class LLM:
    def __init__(self, model):
        self.model = model

    def response(self, prompt: str, history: list[dict[str, str]] = []):
        messages = history
        messages.append({"role": "user", "content": prompt})

        response = completion(
            model=self.model, messages=messages, api_base="http://localhost:8888/v1", api_key="subscribe_please"
        )
        choice = response.choices[0]
        text = choice.message.content
        usage = response.usage

        # TODO:Fill reasoning token details later
        return ModelResult(
            model=response.model,
            response=text,
            tool_calls=choice.message.tool_calls,
            prompt_tokens=usage.prompt_tokens,
            total_tokens=usage.total_tokens,
            reasoning_tokens=0,
        )
