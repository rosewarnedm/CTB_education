from openai import OpenAI
from .anonymise import redact_names_numbers_dates


def getOpenAIresponse(text, model = 'gpt-4o-mini') :
    client = OpenAI()
    texts = [{"role": "user", "content":  text}]

    completion = client.chat.completions.create(
       model = model,
        temperature = 0,
      messages=texts
     )
    return completion.choices[0].message.content

def getOpenAIresponse_redacted_input(text, model = 'gpt-4o-mini', mode = 'VERBOSE') :
    redacted_text = redact_names_numbers_dates(text, mode)
    client = OpenAI()
    texts = [{"role": "user", "content":  redacted_text}]

    completion = client.chat.completions.create(
       model = model,
        temperature = 0,
      messages=texts
     )
    if mode == 'VERBOSE' :
        print(redacted_text)
    return completion.choices[0].message.content
