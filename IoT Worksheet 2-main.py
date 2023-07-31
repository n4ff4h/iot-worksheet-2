from microbit import *
import music
import radio
radio.config(group=6)
radio.on()

MORSE_CODE_MAPPING = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0"
}

# Music durations
DOT_DURATION = 230
DASH_DURATION = 470

# detect a new letter if incoming signal is greater than 1000ms.
LETTER_THRESHOLD = 1000

buffer = ''  # Incoming morse code signals

started_to_wait = running_time()

def decode(buffer):
    return MORSE_CODE_MAPPING.get(buffer, '?')

while True:
    # Work out how long the device has been waiting for a keypress.
    waiting = running_time() - started_to_wait
    signal = radio.receive()
    
    if button_a.is_pressed():
        display.show('.')
        radio.send('.')
        music.pitch(1200, duration=DOT_DURATION, wait=True)
        sleep(50) # Added to debounce
        display.clear()
        
    elif button_b.is_pressed():
        display.show('-')
        radio.send('-')
        music.pitch(1200, duration=DASH_DURATION, wait=True)
        sleep(50) # Added to debounce
        display.clear()
        
    # Listen over radio for morse code signals
    if signal:
        if signal == '.':
            buffer += '.'
            display.show('.')
            sleep(DOT_DURATION)
            display.clear()
        elif signal == '-':
            buffer += '-'
            display.show('-')
            sleep(DASH_DURATION)
            display.clear()
            
        # Reset waiting time now that a signal has been received
        started_to_wait = running_time()

    # So waiting basically greater than a second and there is a buffer
    elif len(buffer) > 0 and waiting > LETTER_THRESHOLD:
        character = decode(buffer)
        buffer = ''
        display.show(character)