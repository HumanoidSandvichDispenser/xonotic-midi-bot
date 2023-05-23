from enum import Enum
from typing import List
from note import Note


class Instrument(Enum):
    Tuba = 0
    Accordion = 1
    KleinBottle = 2


class Part():
    notes: List[Note]
    instrument: Instrument

    def __init__(self):
        self.notes = list()
        self.instrument = Instrument.Tuba


instrument_map = {
    28: Instrument.Accordion,
    58: Instrument.Tuba,
    59: Instrument.KleinBottle
}
