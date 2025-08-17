from openai import OpenAI
from .anonymise import redact_names_numbers_dates


def getOpenAIresponse(text, model = 'gpt-4o-mini', temperature = 0) :
    client = OpenAI()
    texts = [{"role": "user", "content":  text}]
    completion = client.chat.completions.create(
       model = model,
        temperature = temperature,
      messages=texts
     )
    return completion.choices[0].message.content

def getOpenAIresponse_redacted_input(text, model = 'gpt-4o-mini',
                                     temperature = 0, mode = 'VERBOSE') :
    redacted_text = redact_names_numbers_dates(text, mode)
    if mode == 'VERBOSE' :
        print(redacted_text)
    return getOpenAIresponse(text, model, temperature)
