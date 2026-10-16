from google import genai
from google.genai import types
import os
import time


class OptimizeLLMSQLGemini:
    @staticmethod
    def __client(api_key):
        base_url = os.environ.get("LITELLM_BASE_URL")
        if base_url:
            api_key = os.environ.get("LITELLM_API_KEY", api_key)
            return genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(
                    base_url=base_url,
                    headers={"Authorization": f"Bearer {api_key}"},
                ),
            )
        return genai.Client(api_key=api_key)

    @staticmethod
    def optimize_sql_Gemini_LLM(user_message: str, system_message: str):
        from util.Config import _LLM_API_Key
        _, api_key = _LLM_API_Key.get_API_Key()
        client = OptimizeLLMSQLGemini.__client(api_key)
        code, funcs, number_of_tokens, time_gen = OptimizeLLMSQLGemini.__submit_Request_Gemini_LLM(user_message=user_message, system_message=system_message, client=client)
        return code, funcs, number_of_tokens, time_gen

    @staticmethod
    def __submit_Request_Gemini_LLM(user_message: str, system_message: str, client, attempt: int = 0):
        from util.Config import _LLM_API_Key, _llm_model, _temperature, _top_p, _top_k, _max_out_token_limit

        time_start = time.time()
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)],
            )
        ]

        generation_config = types.GenerateContentConfig(
            temperature=_temperature,
            top_p=_top_p,
            top_k=_top_k,
            max_output_tokens=_max_out_token_limit,
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_CIVIC_INTEGRITY",
                    threshold="BLOCK_LOW_AND_ABOVE",  # Block most
                ),
            ],
            response_mime_type="text/plain",
            system_instruction=[ types.Part.from_text( text=system_message )],
        )

        print(f"[{time.strftime('%H:%M:%S')}] gemini call start attempt={attempt} in_chars={len(user_message) + len(system_message)}", flush=True)
        try:
            response = client.models.generate_content(model=_llm_model,
                    contents=contents,
                    config=generation_config)
            code = response.text
            funcs = None
            if "<FUNCTIONS>" in code and "</FUNCTIONS>" in code:
                begin_key = "<FUNCTIONS>"
                end_key = "</FUNCTIONS>"
                begin_point = code.find(begin_key)
                end_point = code.find(end_key)
                funcs = code[begin_point + len(begin_key): end_point]

            begin_key = "```sql"
            end_key = "```"[::-1]
            begin_point = code.find(begin_key)
            if begin_point == -1:
                begin_key = "```\nsql"
                begin_point = code.find(begin_key)

            end_point = len(code) - code[::-1].find(end_key)
            code = code[begin_point+len(begin_key):end_point- len(end_key)]

            time_end = time.time()
            print(f"len text = {len(user_message) + len(system_message)}  , input tokens = {response.usage_metadata.total_token_count} -- {response.usage_metadata.prompt_token_count}")
            return code, funcs, response.usage_metadata.total_token_count, time_end - time_start

        except Exception as err:
            print(f"[{time.strftime('%H:%M:%S')}] gemini call FAILED attempt={attempt} {type(err).__name__}: {err}", flush=True)
            _, api_key = _LLM_API_Key.get_API_Key()
            client = OptimizeLLMSQLGemini.__client(api_key)
            return OptimizeLLMSQLGemini.__submit_Request_Gemini_LLM(user_message=user_message, system_message=system_message, client=client, attempt=attempt + 1)

    @staticmethod
    def get_number_tokens(messages: str):

        from util.Config import _LLM_API_Key, _llm_model

        _, api_key = _LLM_API_Key.get_API_Key()
        client = OptimizeLLMSQLGemini.__client(api_key)
        return client.models.count_tokens(model=_llm_model, contents=messages).total_tokens
