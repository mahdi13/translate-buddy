# Translate Buddy

**This project is just a hobby, the source code is not even close to the "clean"!**

This projects helps you to communicate verbally in writing, using two different languages.

What you have to do is:

1. Read the input text (Your language)
2. Write the response (Your language)

What the audience have to do is to:

1. Talk to you (His/Her language)
2. Listen to you (His/Her language)

## Usecase:

* Communicate realtime with a foreign person over the phone
* For disabled persons, to communicate to another person via speaking

### How does it work

There are two main part:

#### First, listening:

1. Your microphone listen to the input audio
2. The code translates it to your chosen language
3. It prints the text for you in the console

#### Second, speaking:

1. You write a text in your own language
2. The code translate in to your audiences language
3. Read out loud the translated text for your audience

These two process are looping asynchronously.

## Requirements

This code is only compatible with 3 Google clooud services, so you have to make sure they are ready before running the
app:

* [Google cloud speech to text](https://cloud.google.com/speech-to-text)
* [Google cloud Translate](https://cloud.google.com/translate)
* [Google cloud Text to Speach](https://cloud.google.com/text-to-speech)

## Installation (on Ubuntu)

```shell
apt-get install portaudio19-dev
python3.7 -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
python3 main.py
```