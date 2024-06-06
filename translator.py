import os
import openai
import sys
sys.path.append('../..')
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

openai.api_key = os.environ['OPENAI_API_KEY']

def get_translation(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message.content


def main():
    source_lang = "Portuguese"
    target_lang = "English"

    print(f"Welcome! I'm your english teacher for today! I'll help you translate messages in {source_lang} to {target_lang}.")

    user_message = input("How can I help you today? ")
    moderation_input = openai.moderations.create(input=user_message)

    if moderation_input.results[0].flagged:
        return print("Sorry, we cannot process this request.")

    system_message = f"""
    You're a {target_lang} teacher. Your task is correctly translate the message the user gives you in {source_lang} to {target_lang}, in a cheerful tone. You have to provide the user some helpful tips and further explanation on the translation, giving some more insight and tips on {target_lang}. Respond in a friendly and helpful tone, with concise answers. Don't congratulate the user on the sucessful translation. Don't make up things you don't know.
    """

    example_input_1 = """
    traduzir "Vamos marcar uma reunião"
    """
    example_output_1 = """
    "Let's schedule a meeting."
    In English, the verb "to schedule" is commonly used when setting up appointments, meetings, or events. It's a versatile word that can be used in various contexts. Remember to use "let's" before the verb to suggest doing something together. Keep up the good work!
    """

    messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': example_input_1},
    {'role': 'assistant', 'content': example_output_1},
    {'role': 'user', 'content': user_message}
    ]

    translation = get_translation(messages)
    moderation_output = openai.moderations.create(input=translation)

    if moderation_output.results[0].flagged:
        return print("Sorry, we cannot process this request.")

    print("\nTeacher:")
    print(translation)

if __name__ == "__main__":
    main()