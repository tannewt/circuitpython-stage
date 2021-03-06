"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

import board
import digitalio
import busio
import audioio
import analogio

import st7735r
import gamepad


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20


class Audio:
    last_audio = None

    def __init__(self):
        self.mute_pin = digitalio.DigitalInOut(board.MUTE)
        self.mute_pin.switch_to_output(value=1)

    def play(self, audio_file):
        self.stop()
        self.last_audio = audioio.AudioOut(board.SPEAKER, audio_file)
        self.last_audio.play()

    def stop(self):
        if self.last_audio:
            self.last_audio.stop()

    def mute(self, value=True):
        self.mute_pin.value = not value


dc = digitalio.DigitalInOut(board.DC)
cs = digitalio.DigitalInOut(board.CS)
cs.switch_to_output(value=1)
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
spi.try_lock()
spi.configure(baudrate=24000000, polarity=0, phase=0)
cs.value = 0
display = st7735r.ST7735R(spi, dc, 0b101)

buttons = gamepad.GamePad(
    digitalio.DigitalInOut(board.X),
    digitalio.DigitalInOut(board.DOWN),
    digitalio.DigitalInOut(board.LEFT),
    digitalio.DigitalInOut(board.RIGHT),
    digitalio.DigitalInOut(board.UP),
    digitalio.DigitalInOut(board.O),
)

audio = Audio()

battery = analogio.AnalogIn(board.BATTERY)
