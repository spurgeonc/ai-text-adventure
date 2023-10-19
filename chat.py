import os
import openai
import random
import shutil

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")
num = random.randint(0, 9999)
filename = 'archives/file%d.txt' % num
f = open(filename, 'a')
history = []
print(f'(saving to ' + filename + ')\n(type "exit" to quit)')
cont = True

while (cont):
    # Get user input for the prompt
    user_prompt = input("Enter your prompt: ")
    if (user_prompt == 'exit'):
        cont = False
    chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[
        {"role": "system", "content": "You are a helpful assistant for an undergarduate computer science student. Your wrapper program has an 'exit' command that stops the chat and saves the convo to a file."}, 
        *history,
        {"role": "user", "content": user_prompt},
    ])

    history.append({"role": "user", "content": user_prompt})
    f.write('USER:\n' + user_prompt + '\n')

    # Print the response from the AI model
    print(chat_completion["choices"][0]["message"]["content"])
    history.append({"role": "assistant", "content": chat_completion["choices"][0]["message"]["content"]})
    f.write('AI:\n' + chat_completion["choices"][0]["message"]["content"] + '\n')
history.pop()
history.pop()
chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[
        {"role": "system", "content": "You are a program that makes filenames for .txt files. Respond with [filename].txt and nothing else, based on the following conversation (do not include the word 'exit'):"}, 
        *history,
    ])
filename2 = chat_completion["choices"][0]["message"]["content"]
print('(archives/' + filename2 + ')')
f2 = open('archives/' + filename2, 'a')
f.close()
os.remove(filename)
current_speaker = "USER:\n"
count = 0
for i in history:
    if (count % 2 == 0):
        current_speaker = "USER:\n"
    else:
        current_speaker = "AI:\n"
    f2.write(current_speaker)
    f2.write(i["content"])
    f2.write('\n\n')
    count = count + 1

f2.close()