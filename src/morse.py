import array
import math
import sys
import time

import pyaudio

p = pyaudio.PyAudio()

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
f = 440.0  # sine frequency, Hz, may be float
stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

dot_duration = 0.25
dash_duration = 3 * dot_duration
CHAR_PAUSE_DURATION = 0.8 * dash_duration
ELEMENT_PAUSE_DURATION = dot_duration # this is for every dot or dash
WORD_PAUSE_DURATION = 2 * CHAR_PAUSE_DURATION

# thank you to https://www.geeksforgeeks.org/python/morse-code-translator-python/
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----'}



def play_cw(duration=0.1):
    # generate samples, note conversion to float32 array
    num_samples = int(fs * duration)
    samples = [volume * math.sin(2 * math.pi * k * f / fs) for k in range(0, num_samples)]

    output_bytes = array.array('f', samples).tobytes()

    stream.write(output_bytes)

def play_morse_char(input: str):
    if len(input) > 1:
        return play_morse_str(input)

    # ignore if this isn't a valid character
    if input.upper() not in MORSE_CODE_DICT:
        print("DEBUG: not a real char")
        return

    # handle letter pause for sanity
    time.sleep(CHAR_PAUSE_DURATION) 

    print(input)
    
    for dot_or_dash in MORSE_CODE_DICT[input.upper().strip()]:
        time.sleep(ELEMENT_PAUSE_DURATION) # more sanity stuff

        # play each letter
        play_dot_or_dash(dot_or_dash)



def play_dot_or_dash(input: str):
    if len(input) > 1:
        print("ERROR: called play_dot_or_dash() which expects only one character, using multiple characters.")
        sys.exit(1)

    if input == ".":
        return play_cw(dot_duration)
    elif input == "-":
        return play_cw(dash_duration)



def play_morse_str(input: str):
    for letter in input:
        # handle word pauses for sanity
        if letter == " ":
            return time.sleep(WORD_PAUSE_DURATION - CHAR_PAUSE_DURATION) # subtracting that because the letter pause happens every time

        play_morse_char(letter)


def main():
    try:
        play_morse_str("Hello, World!")
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    main()
