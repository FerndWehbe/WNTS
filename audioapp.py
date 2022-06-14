import pyaudio
import numpy
import json


RATE = 44100
CHUNK = 1024 * 4


with open("./config.json") as f:
    notes = json.load(f)


def calcule_note_range(tolerance: int = 33) -> dict:
    tolerance_multiplier = 2 ** (tolerance / 1200)
    note_ranges = {}
    for key, value in notes["notes"].items():
        note_ranges[key] = (
            value / tolerance_multiplier,
            value * tolerance_multiplier,
        )
    with open("note_range.json", "w") as f:
        json.dump(note_ranges, f, indent=4)
    return note_ranges


def get_freq(data: numpy.array) -> None | float:
    if not data:
        return None
    dt = numpy.frombuffer(data, dtype=numpy.float32)
    if not dt[0]:
        return None
    fftdata = abs(numpy.fft.rfft(dt)) ** 2
    max_val = fftdata[1:].argmax() + 1
    if max_val != len(fftdata) - 1:
        y0, y1, y2 = numpy.log(fftdata[max_val - 1 : max_val + 2])
        x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 - y0)
        freq = (max_val + x1) * RATE / CHUNK
        return freq


def get_note_from_freq(freq: float, note_range: dict) -> str | None:
    min_freq = note_range["C0"][0]
    max_freq = note_range["B8"][1]
    if freq < min_freq or freq > max_freq:
        return None

    for note, note_range in note_range.items():
        if freq > note_range[0] and freq < note_range[1]:
            return note
    return None


def runn_app(index: int) -> None:
    audio = pyaudio.PyAudio()

    try:
        with open("./note_range.json") as f:
            note_range = json.load(f)
    except FileNotFoundError:
        note_range = calcule_note_range()

    def get_stream() -> bytes:
        stream = audio.open(
            input_device_index=index,
            format=pyaudio.paFloat32,
            channels=1,
            rate=RATE,
            frames_per_buffer=CHUNK,
            input=True,
        )
        wf_data = stream.read(CHUNK)
        return wf_data

    running = True
    while running:
        stream_data = get_stream()
        freq = get_freq(stream_data)
        try:
            frequency = numpy.ceil(freq)
            note = get_note_from_freq(frequency, note_range)
            if note:
                print(f"{frequency}hz <-> {note}")
        except TypeError:
            pass
