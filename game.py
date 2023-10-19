import os
import openai
import random
import shutil

openai.api_key = os.getenv("OPENAI_API_KEY")

current_room = 0
NORTH = 0
WEST = 1
EAST = 2
SOUTH = 3



def numToDir(int):
    if (int == NORTH):
        return "North"
    else:
        if (int == WEST):
            return "West"
        else: 
            if (int == EAST):
                return "East"
            else: 
                if (int == SOUTH):
                    return "South"
                else:
                    return "N/A"

class Room:
    def __init__(self, name, objects, entrance):
        self.name = name
        self.objects = objects
        self.entrance = entrance
        self.north = 0
        self.west = 0
        self.east = 0
        self.south = 0
        self.exits = [self.north, self.west, self.east, self.south]
        self.examined = False
    
    def examine(self):
        if self.examined == False:
            localcount = 0
            while localcount < 4:
                coinflip = random.randint(1, 2)
                if coinflip == 2:
                    self.exits[localcount] = Room("EmptyRoom", [], [])
                else:
                    self.exits[localcount] = self
                localcount = localcount + 1
            
        
        localcount = 0
        exits_string = ""
        objects_string = ""
        for i in self.objects:
            objects_string = objects_string + "a " + i + ", "
        objects_string = objects_string[:-2]
        str_list = objects_string.rsplit(', ', 1)  # Splitting from the right side
        str_modified = ' and '.join(str_list)  # Joining with 'and'
        objects_string = str_modified + "."
        while (localcount < 4):
            exits_string = exits_string + "\nTo the " + numToDir(localcount) + " is a " + self.exits[localcount].name
            localcount = localcount + 1
        localcount = 0
        print("You are in a", self.name, "\nIn the area is", objects_string, exits_string)

        self.examined = True

    def load(self):
        current_room = self

menu = Room("Menu", [], [])
current_room = menu

def run(string):
    global current_room
    print(string)
    known_command = False

    if current_room.name == "Menu":
        if (string == "1" or string == "New Game"):
            current_room = Room("Bedroom", ["Bed", "Desk", "Computer", "Window", "Closet"], [])
            current_room.examine()

    if (string == "examine" or string == "examine room"):
        current_room.examine()

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

#

game_running = True


print("Welcome to BotQuest, a procedurally-generated, AI-written RPG!\n\n1. New Game\n2. Load Game \n3. Settings \n4. Help\n5. Exit")
while (game_running):
    new_command = input("")
    run(new_command)

def chat(chat_prompt):
    num = random.randint(0, 9999)
    filename = 'archives/file%d.txt' % num
    f = open(filename, 'a')
    history = []
    cont = True
    print(f'(saving to ' + filename + ')\n(type "!exit" to quit)')
    while (cont):
        chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[
            {"role": "system", "content": chat_prompt + "Your wrapper program has a !exit command."}, 
            *history,
        ])

        # Print the response from the AI model
        print(chat_completion["choices"][0]["message"]["content"])
        history.append({"role": "assistant", "content": chat_completion["choices"][0]["message"]["content"]})
        f.write('AI:\n' + chat_completion["choices"][0]["message"]["content"] + '\n')
        # Get user input for the prompt
        user_prompt = input("Enter your prompt: ")
        history.append({"role": "user", "content": user_prompt})
        if (user_prompt == '!exit'):
            cont = False
        f.write('USER:\n' + user_prompt + '\n')
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