"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random

counter = {'key':0}
## greeting words
USER_GREETING = ["hey", "good", "how are you","what's up", "what's new","okay"]
BOT_GREETING = ["hi", "what gossip do you have for me?", "what would you like to talk about","I hope you're more entertaining than the last person who tried to talk to me"]

## swear words
SWEAR_WORDS = ["bitch","dicked","cock","fuck","pussy","stupid"]

## if robot doesn't understand
DONT_UNDERSTAND = ["I have no idea what you're on about","I speak more lanugages than just coding","Sorry can you speak English?",
                   "Have you smoked something today?"]

## if user is mean to the robot
USER_MEAN = ["I thought you'd be more fun","This sucks","Do you have nothing else to say","KK","Anything else to say?","You've already said that","And what"]
HURT_BOT = ["Look, I'm sorry you're bored, I'm a basic chatbot created by some 26 year old. Please be gentle with me",
              "You don't have to be mean! Robots have feelings too.", "Oi! Don't be so aggressive.", "YOLO"]

## if user thinks robot is being mean
USER_HURT = ["rude", "relax", "mean","fisty one today Robo"]
BOT_APOLOGY = ["why you so sensitive, LMAO", "grow up, real life will be like this","I apologize, can we move on?","Lets be friends please"]

## if user wants to move on
USER_CONVO = ["sorry","yes","nothing new","no gossip","that's fun","im good","good","ok"]
BOT_CONVO_ANSWER = ["Ok moving on, what do you want to talk about now?","Can we move to the next topic please?","Yalla, Yalla"]

## if user response is yes or no
YES_NO = ["yes", "no", "yep","yup", "nope"]
BOT_YES_NO = ["But like same though, let's talk about something else","I feel the exact same way! Ask me to do something robots do", "I can do cool things too you know"]

## if user asks a question
USER_QUESTIONMARK = ["That's pretty personal","How would you feel if I asked you a question like that?","That's too deep","I have my limits!"]

def greeting(user_message):
    for word in USER_GREETING:
        if word == user_message:
            message = random.choice(BOT_GREETING)
            return message
    return None

def swear(user_message):
    for word in SWEAR_WORDS:
        if word in user_message:
            message = "Say " + user_message + " one more time, see what happens!"
            return message
    return None

def mean(user_message):
    for word in USER_MEAN:
        if word in user_message:
            message = random.choice(HURT_BOT)
            return message
    return None

def rude(user_message):
    for word in USER_HURT:
        if word in user_message:
            message = random.choice(BOT_APOLOGY)
            return message
    return None

def convoStarter(user_message):
    for word in USER_CONVO:
        if word in user_message:
            message = random.choice(BOT_CONVO_ANSWER)
            return message
    return None

def yesOrNo(user_message):
    for word in YES_NO:
        if word in user_message:
            message = random.choice(BOT_YES_NO)
            return message
    return None

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()

    ## special greetings for people called Nath
    if user_message == "Charlotte":
        return json.dumps({"animation": "giggling", "msg": "Was that english?"})

    ## first greeting with name
    elif counter['key'] == 0:
        counter['key'] += 1
        return json.dumps({"animation": "excited", "msg": "OMG " + user_message + ", That's my favorite name ever. What is new in your life " + user_message + "?"})

    elif "?" in user_message:
        message = random.choice(USER_QUESTIONMARK)
        return json.dumps({"animation": "no", "msg": message})

    elif "you" in user_message:
        return json.dumps({"animation": "laughing", "msg": "I know you are but what am I"})

    elif "weather" in user_message:
        return json.dumps(
            {"animation": "dog", "msg": "I don't know, but you should stay indoors, I heard you burn easily"})

    elif "food" in user_message:
        return json.dumps(
            {"animation": "excited", "msg": "STOP! I love food too. Food friends for life?"})

    ## any greetings from user
    greeting_result = greeting(user_message)
    if greeting_result is not None:
        return json.dumps({"animation": "bored", "msg": greeting_result})

    ## if a user swears
    swear_result = swear(user_message)
    if swear_result is not None:
        return json.dumps({"animation": "no", "msg": swear_result})

    ## if user is being mean
    mean_result = mean(user_message)
    if mean_result is not None:
        return json.dumps({"animation": "crying", "msg": mean_result})

    ## if bot is being mean
    rude_result = rude(user_message)
    if rude_result is not None:
        return json.dumps({"animation": "afraid", "msg": rude_result})

    ## if conversation is lacking
    convo_starter = convoStarter(user_message)
    if convo_starter is not None:
        return json.dumps({"animation": "bored", "msg": convo_starter})

    ## basic yes or no answers
    yesOrNo_result = yesOrNo(user_message)
    if yesOrNo_result is not None:
        return json.dumps({"animation": "dancing", "msg": yesOrNo_result})

    else:
        message = random.choice(DONT_UNDERSTAND)
        return json.dumps({"animation": "dog", "msg": message})

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
