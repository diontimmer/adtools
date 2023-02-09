import sf2_loader as sf
import os
import pydub
from tqdm import tqdm
import argparse

def get_all_notes():
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	octaves = list(range(0,10))
	notes_with_octaves = []
	for note in notes:
		for octave in octaves:
			notes_with_octaves.append(note + str(octave))
	return notes_with_octaves

def export_soundfont(loader, soundfont_path, output_folder, raw=False):
	if loader.sfid_list:
		loader.unload(1)
	soundfont_name = os.path.basename(soundfont_path).split('.')[0]
	print(f'Exporting SF: {soundfont_name}..')
	loader.load(soundfont_path)
	inst_dict = loader.all_instruments()
	banks = list(inst_dict.keys())
	for bank in banks:
		loader.change_bank(bank)
		presets = list(inst_dict[bank])
		prog = tqdm(presets)
		for preset in prog:
			preset_name = inst_dict[bank][preset].replace(' ', '')
			prog.set_postfix({'preset': preset_name})
			loader.change_preset(preset)
			notes = get_all_notes()
			for note in notes:
				if not os.path.exists(f'{output_folder}/{soundfont_name}/bank_{bank}/{preset_name}'):
					os.makedirs(f'{output_folder}/{soundfont_name}/bank_{bank}/{preset_name}')
				out_path = os.path.join(f'{output_folder}/{soundfont_name}/bank_{bank}/{preset_name}/{preset_name}_{note}.wav')
				audio = loader.export_note(note, name=out_path, format='wav', get_audio=True)
				if audio.dBFS > -80:
					if not raw:
						audio = pydub.effects.normalize(audio)
					audio.export(out_path, format='wav')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export Soundfont as WAV files')
    parser.add_argument('soundfont_path', type=str, help='Path to the soundfont file')
    parser.add_argument('output_folder', type=str, help='Output folder to save the WAV files')
    parser.add_argument('--raw', action='store_true', help='Do not normalize the audio files')
    args = parser.parse_args()
    loader = sf.sf2_loader()
    export_soundfont(loader, args.soundfont_path, args.output_folder, args.raw)