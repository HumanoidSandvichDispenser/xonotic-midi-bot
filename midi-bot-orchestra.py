#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 sandvich <sandvich@manjaro>
#
# Distributed under terms of the GPL3 license.

import sys
import typing
from mido import MidiFile, MidiTrack, Message, tick2second, second2tick
import click
import notemap
from notemap import note_map, TubaInput
from note import Note
from part import Part, Instrument


@click.command()
@click.argument("filename")
@click.argument("delay", default=0)
@click.option("-p", "--transpose", type=int, default=0)
@click.option(
        "--header/--no-header",
        help="Includes a header containing the aliases for bots to play notes",
        type=bool, default=False)
def main(filename: str, delay: int, transpose: int, header: bool):
    midi = MidiFile(filename, clip=True)

    print("// autogenerated by HumanoidSandvichDispenser's MIDI CFG script")

    if header:
        generate_header()
        return

    tempo: int = 500000
    track: MidiTrack

    parts: typing.List[Part] = []

    for i, track in enumerate(midi.tracks):
        #notes: typing.List[Note] = [ ]
        part: Part = Part()
        message: Message
        prev_note: Note = None

        # 8 second delay to give bots time to switch instruments
        elapsed = delay + second2tick(8, midi.ticks_per_beat, tempo)

        if track.name == "Accordion\x00":
            part.instrument = Instrument.Accordion
        elif track.name == "Klein Bottle\x00":
            part.instrument = Instrument.KleinBottle
        else: # everything else defaults to tuba
            part.instrument = Instrument.Tuba

        for message in track:
            elapsed += message.time
            elapsed_seconds = tick2second(elapsed, midi.ticks_per_beat, tempo)
            if message.type == "note_on":
                note_pitch = message.note + transpose

                if part.instrument == Instrument.Accordion:
                    # tranpose 8vb since they play an octave above than what
                    # the note calls (e.g. plays C4 instead of C3)
                    note_pitch -= 12
                elif part.instrument == Instrument.KleinBottle:
                    note_pitch += 12

                if note_pitch not in notemap.note_input_map:
                    print("[WARN] Note %d is out of range. (#%d instr. %s)" %
                          (note_pitch, i, track.name), file=sys.stderr)
                    continue  # skip attempting to play it

                if notemap.note_input_map[note_pitch] == \
                        TubaInput.UNSUPPORTED:
                    print("[WARN] Note %d %s is unsupported. (#%d instr. %s)" %
                          (note_pitch, note_map[note_pitch], i, track.name),
                          file=sys.stderr)
                    continue

                if message.velocity > 0:  # a new note is being played
                    if prev_note != None:
                        print("[WARN] Another note has been found playing " +
                              "concurrently; ignoring note %d %s (#%d instr. %s)" %
                              (note_pitch, note_map[note_pitch], i, track.name),
                              file=sys.stderr)
                        continue
                    note = Note()
                    note.location = elapsed_seconds
                    note.pitch = note_pitch

                    prev_note = note
                else:  # a note is ending
                    if prev_note != None:
                        if prev_note.pitch == note_pitch: # matches; they are the same note
                            # detache in case new notes (from defer) are pushed
                            # to the bot's command queue before the bot stops
                            # playing its current note.
                            full_length = elapsed_seconds - prev_note.location
                            detache_length = full_length - 0.1
                            half_length = full_length * 0.5

                            # detache if note is long enough, half length if too short
                            prev_note.length = max(detache_length, half_length)

                            part.notes.append(prev_note)
                            prev_note = None
            elif message.type == "set_tempo":
                pass

        parts.append(part)
    if header:
        generate_header()
    # finally we generate config based on the notes we parsed
    generate_cfg(parts)

def generate_cfg(tracks: typing.List[Part]):
    #print("bot_number %d; wait;" % len(tracks))

    for i, part in enumerate(tracks):
        bot_num = i + 1
        id = len(tracks) + 2 - bot_num
        print(("bot_cmd {0} wait 1; bot_cmd {0} cc give tuba;" +
               "bot_cmd {0} impulse 244;").format(bot_num, id))

        # switch instrument if necessary (with reload button)
        if part.instrument == Instrument.Accordion:
            print("bot_cmd {0} wait 1; bot_cmd {0} impulse 20;".format(bot_num))
        elif part.instrument == Instrument.KleinBottle:
            print("bot_cmd {0} wait 1; bot_cmd {0} impulse 20; bot_cmd {0} wait 1; bot_cmd {0} impulse 20;"
                  .format(bot_num))
        for note in part.notes:
            print("defer_tubabot_%d %d %f %f" % (note.pitch,
                                                 bot_num,
                                                 note.location,
                                                 note.length))


# usage: defer_tubabot_[note index] [bot num] [location] [length]
# example output
# alias defer_tubabot_50 "defer $2 \"bot_cmd $1 presskey +right; bot_cmd $1 presskey +crouch; bot_cmd $1 presskey +attack1; bot_cmd $1 wait $3; bot_cmd $1 releasekey all;\""

def generate_header():
    for note_index, inputs in notemap.note_input_map.items():
        alias_format = "alias defer_tubabot_%d \"%s\""
        defer = ""
        defer_format = "defer $2 \\\"%s\\\""
        commands = ""
        commands_format = "bot_cmd $1 %s %s;"
        commands += commands_format % ("releasekey", "all")

        print()
        if inputs != TubaInput.UNSUPPORTED:
            if (TubaInput.FORWARD in inputs):
                commands += commands_format % ("presskey", "forward")
            elif (TubaInput.BACK in inputs): # mutually exclusive to FORWARD
                commands += commands_format % ("presskey", "backward")

            if (TubaInput.LEFT in inputs):
                commands += commands_format % ("presskey", "left")
            elif (TubaInput.RIGHT in inputs):
                commands += commands_format % ("presskey", "right")

            if (TubaInput.JUMP in inputs):
                commands += commands_format % ("presskey", "jump")
            elif (TubaInput.CROUCH in inputs):
                commands += commands_format % ("presskey", "crouch")

            if (TubaInput.ATTACK1 in inputs):
                commands += commands_format % ("presskey", "attack1")
            elif (TubaInput.ATTACK2 in inputs): # mutually exclusive to ATTACK1
                commands += commands_format % ("presskey", "attack2")

            commands += commands_format % ("wait", "$3")
            commands += commands_format % ("debug_assert_canfire", "0")

        # this is a workaround to bots releasing the attack key after the movement keys
        # you can see the bot stops attacking before stopping movement in bot_cmd_pause function
        # http://timepath.github.io/scratchspace/d6/d27/scripting_8qc.html#ae45866653ec08ae20bf0398f42023dc7
        # 
        # BUT... using bot_cmd_releasekey will actually release movement keys before attack1
        # resulting in a short middle C note when the bot stops playing

        commands += commands_format % ("pause", "")
        commands += commands_format % ("continue", "")
        #commands += commands_format % ("releasekey", "all") <- bad
        defer = defer_format % commands
        print(alias_format % (note_index, defer))

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
