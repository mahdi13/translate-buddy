import signal
import sys
import threading
from queue import Queue

from playsound import playsound
from google.cloud import texttospeech

written_lang = 'en'
spoken_lang = 'tr'
spoken_lang_code = 'tr-TR'
voice = texttospeech.VoiceSelectionParams(
    language_code='tr-TR',
    name='tr-TR-Wavenet-B',
    ssml_gender=texttospeech.SsmlVoiceGender.MALE,
)


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]


def readout(text):
    """Synthesizes speech from the input string of text."""

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')
    playsound("output.mp3")


def kill_signal_handler(signal_number, _):
    if signal_number == signal.SIGINT:
        print('You pressed Ctrl+C!')
    elif signal_number in (signal.SIGTERM, signal.SIGKILL):
        print('OS Killed Me!')

    sys.stdin.close()
    sys.stderr.close()
    sys.stdout.close()
    sys.exit(1)


def readouter(language_code, q_: Queue = None):
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        readout(translate_text(language_code, line))


def translator(language_code, q_: Queue = None):
    while True:
        dialogue = q_.get()
        # print(f'Translating {dialogue}')
        print(translate_text(language_code, text=dialogue))
        q_.task_done()


def launch(q_: Queue):
    signal.signal(signal.SIGINT, kill_signal_handler)
    signal.signal(signal.SIGTERM, kill_signal_handler)

    from listen import live_listen
    t = threading.Thread(
        target=live_listen,
        name='live_listen',
        daemon=True,
        kwargs=dict(
            language_code=spoken_lang_code,
            q_=q_,
        )
    )
    t.start()

    t = threading.Thread(
        target=translator,
        name='translator',
        daemon=True,
        kwargs=dict(
            language_code=written_lang,
            q_=q_,
        )
    )
    t.start()

    t = threading.Thread(
        target=readouter,
        name='readouter',
        daemon=True,
        kwargs=dict(
            language_code=spoken_lang
        )
    )
    t.start()

    print(f'TranslateBuddy started!')
    print('Press Ctrl+C to terminate')
    signal.pause()


if __name__ == '__main__':
    q = Queue()
    launch(q)
