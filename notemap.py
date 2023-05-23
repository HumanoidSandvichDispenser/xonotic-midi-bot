#! /usr/bin/echo This python module is not meant to be run
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 sandvich <sandvich@manjaro>
#
# Distributed under terms of the GPL3 license.


from enum import IntFlag


class TubaInput(IntFlag):
    UNSUPPORTED = 0 # check for equality
    LEFT = 1
    RIGHT = 2
    BACK = 4
    FORWARD = 8
    CROUCH = 16
    JUMP = 32
    ATTACK1 = 64
    ATTACK2 = 128

LEFT = TubaInput.LEFT
RIGHT = TubaInput.RIGHT
BACK = TubaInput.BACK
FORWARD = TubaInput.FORWARD
CROUCH = TubaInput.CROUCH
JUMP = TubaInput.JUMP
ATTACK1 = TubaInput.ATTACK1
ATTACK2 = TubaInput.ATTACK2

note_input_map = {
    42: TubaInput.LEFT | TubaInput.CROUCH | TubaInput.BACK | TubaInput.ATTACK1,
    43: TubaInput.BACK | TubaInput.CROUCH | TubaInput.ATTACK1,
    44: TubaInput.RIGHT | TubaInput.BACK | TubaInput.CROUCH | TubaInput.ATTACK1,
    45: TubaInput.UNSUPPORTED,
    46: TubaInput.UNSUPPORTED,
    47: TubaInput.FORWARD | TubaInput.RIGHT | TubaInput.CROUCH | TubaInput.ATTACK1,
    48: TubaInput.CROUCH | TubaInput.ATTACK1,
    49: TubaInput.LEFT | TubaInput.BACK | TubaInput.CROUCH | TubaInput.ATTACK2,
    50: TubaInput.RIGHT | TubaInput.CROUCH | TubaInput.ATTACK1,
    51: TubaInput.FORWARD | TubaInput.LEFT | TubaInput.CROUCH | TubaInput.ATTACK1, 
    52: TubaInput.FORWARD | TubaInput.CROUCH | TubaInput.ATTACK1,
    53: TubaInput.LEFT | TubaInput.CROUCH | TubaInput.ATTACK1,
    54: TubaInput.LEFT | TubaInput.BACK | TubaInput.ATTACK1,
    55: TubaInput.BACK | TubaInput.ATTACK1,
    56: TubaInput.BACK | TubaInput.RIGHT | TubaInput.ATTACK1,
    57: TubaInput.RIGHT | TubaInput.CROUCH | TubaInput.ATTACK2,
    58: TubaInput.FORWARD | TubaInput.LEFT | TubaInput.CROUCH | TubaInput.ATTACK2,
    59: TubaInput.FORWARD | TubaInput.RIGHT | TubaInput.ATTACK1,
    60: TubaInput.ATTACK1,
    61: TubaInput.LEFT | TubaInput.BACK | TubaInput.ATTACK2,
    62: TubaInput.RIGHT | TubaInput.ATTACK1,
    63: TubaInput.FORWARD | TubaInput.LEFT | TubaInput.ATTACK1,
    64: TubaInput.FORWARD | TubaInput.ATTACK1,
    65: TubaInput.LEFT | TubaInput.ATTACK1,
    66: TubaInput.FORWARD | TubaInput.RIGHT | TubaInput.ATTACK2,
    67: TubaInput.ATTACK2,
    68: TubaInput.BACK | TubaInput.RIGHT | TubaInput.JUMP | TubaInput.ATTACK1,
    69: TubaInput.RIGHT | TubaInput.ATTACK2,
    70: TubaInput.FORWARD | TubaInput.LEFT | TubaInput.ATTACK2,
    71: TubaInput.FORWARD | TubaInput.ATTACK2,
    72: TubaInput.LEFT | TubaInput.ATTACK2,
    73: TubaInput.LEFT | TubaInput.BACK | TubaInput.JUMP | TubaInput.ATTACK2,
    74: TubaInput.RIGHT | TubaInput.JUMP | TubaInput.ATTACK1,
    75: TubaInput.FORWARD | TubaInput.LEFT | TubaInput.JUMP | TubaInput.ATTACK1,
    76: TubaInput.FORWARD | TubaInput.JUMP | TubaInput.ATTACK1,
    77: TubaInput.LEFT | TubaInput.JUMP | TubaInput.ATTACK1,
    78: TubaInput.FORWARD | TubaInput.RIGHT | TubaInput.JUMP | TubaInput.ATTACK2,
    79: TubaInput.JUMP | TubaInput.ATTACK2,
    80: TubaInput.UNSUPPORTED,
    81: TubaInput.RIGHT | TubaInput.JUMP | TubaInput.ATTACK2,
    82: TubaInput.FORWARD | TubaInput.LEFT | TubaInput.JUMP | TubaInput.ATTACK2,
    83: TubaInput.FORWARD | TubaInput.JUMP | TubaInput.ATTACK2,
    84: TubaInput.LEFT | TubaInput.JUMP | TubaInput.ATTACK2
}

note_map = {
    42: "F#",
    43: "G",
    44: "G#",
    45: "A",
    46: "A#",
    47: "B",
    48: "C",
    49: "C#",
    50: "D",
    51: "D#",
    52: "E",
    53: "F",
    54: "F#",
    55: "G",
    56: "G#",
    57: "A",
    58: "A#",
    59: "B",
    60: "C",
    61: "C#",
    62: "D",
    63: "D#",
    64: "E",
    65: "F",
    66: "F#",
    67: "G",
    68: "G#",
    69: "A",
    70: "A#",
    71: "B",
    72: "C",
    73: "C#",
    74: "D",
    75: "D#",
    76: "E",
    77: "F",
    78: "F#",
    79: "G",
    80: "G#",
    81: "A",
    82: "A#",
    83: "B",
    84: "C"
}
