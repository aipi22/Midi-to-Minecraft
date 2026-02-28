import mido
from collections import defaultdict
import os

path = os.path.expanduser(
    "~/Library/Application Support/minecraft/saves/test/datapacks/music/data/music/function/tick.mcfunction"
)

INSTRUMENTS = {
    0: {'wave': 'minecraft:block.note_block.bit', 'volume': 1.0},
    1: {'wave': 'minecraft:block.note_block.snare', 'volume': 0.5},
    2: {'wave': 'minecraft:block.note_block.didgeridoo', 'volume': 1.0},
    9: {'wave': 'minecraft:block.note_block.snare', 'volume': 1.0},
}

pitch_shift = 0

timeline = defaultdict(list)

def midi_to_pitch(note_number):
    note_number -= pitch_shift
    pitch = 2 ** ((note_number - 66) / 12)
    return max(0.5, min(2.0, pitch))


def play_midi(file_path):
    mid = mido.MidiFile(file_path)
    print(f"Processing MIDI: {file_path}")

    timeline.clear()
    absolute_time_seconds = 0.0

    for msg in mid:
        absolute_time_seconds += msg.time

        current_mc_tick = int(round(absolute_time_seconds * 20)) + 1

        if msg.type == 'note_on' and msg.velocity > 0:
            pitch = midi_to_pitch(msg.note)
            channel = msg.channel

            instrument = INSTRUMENTS.get(channel, {'wave': 'minecraft:block.note_block.chime', 'volume': 0.2})
            volume = (msg.velocity / 127) * instrument['volume']

            timeline[current_mc_tick].append(
                f"playsound {instrument['wave']} master @a ~ ~ ~ {volume:.3f} {pitch:.3f}"
            )

        if msg.type == 'note_off':
            channel = msg.channel

            instrument = INSTRUMENTS.get(channel, {'wave': 'minecraft:block.note_block.chime', 'volume': 0.2})

            timeline[current_mc_tick].append(
                f"stopsound @a master {instrument['wave']}"
            )

    return timeline

def generate(final_timeline):
    final = ["scoreboard players add #t music_tick 1\n"]
    for tick in sorted(final_timeline):
        for cmd in final_timeline[tick]:
            final.append(f"execute if score #t music_tick matches {tick} run {cmd}\n")
    return "".join(final)

if __name__ == "__main__":
    try:
        output = generate(play_midi(''))
        with open(path, "w") as f:
            f.write(output)
        print(f"Written mcfunction file to: {path}")
    except FileNotFoundError:
        print("Error: Please provide a valid .mid file path.")
