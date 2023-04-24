import os
import argparse
import glob
from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm


def cut_audio_files(dir_path, chunk_length_samples, sample_rate, output_folder, min_volume_db=-50):
    # Get a list of all the WAV/FLAC/Mp3 files in the directory (recursively)
    audio_files = glob.glob(os.path.join(dir_path, "**", "*.wav"), recursive=True) + \
                  glob.glob(os.path.join(dir_path, "**", "*.flac"), recursive=True) + \
                  glob.glob(os.path.join(dir_path, "**", "*.mp3"), recursive=True)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop over all files in the list
    prog = tqdm(audio_files)
    for file_path in prog:
        file_name = os.path.basename(file_path)

        # Load the audio file
        audio = AudioSegment.from_file(file_path)

        # Calculate the length of the audio file in milliseconds
        audio_length_ms = len(audio)

        # Calculate the length of the audio file in samples
        audio_length_samples = audio_length_ms * sample_rate // 1000

        # Calculate the length of each chunk in milliseconds
        chunk_length_ms = chunk_length_samples * 1000 // sample_rate

        # Create a generator that yields audio chunks
        audio_chunks = make_chunks(audio, chunk_length_ms)

        # Iterate over each chunk
        prog.set_description(f'Cutting {file_name} into {len(audio_chunks)} chunks.')
        for i, chunk in enumerate(audio_chunks):
            # Calculate the root mean square (RMS) of the chunk
            rms = chunk.rms

            # Check if the RMS value is above the minimum volume threshold
            if rms < 10**(min_volume_db/20):
                print(f"Skipping chunk {i} of {file_name} because its RMS value ({rms}) is below the minimum volume threshold ({min_volume_db} dBFS).")
                continue

            # Save the chunk as a separate file
            chunk.export(os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_chunk_{i}.wav"), format="wav")
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut audio files into chunks")
    parser.add_argument("dir_path", type=str, help="Path to the directory containing the audio files")
    parser.add_argument("chunk_length_samples", type=int, help="Length of each chunk in samples")
    parser.add_argument("sample_rate", type=int, help="Sample rate of the audio files in samples per second")
    parser.add_argument("output_folder", type=str, help="Path to the directory where the cut chunks will be saved")
    parser.add_argument("--min_volume_db", type=float, default=-50, help="Minimum volume threshold in dBFS to save a chunk")
    args = parser.parse_args()
    cut_audio_files(args.dir_path, args.chunk_length_samples, args.sample_rate, args.output_folder, args.min_volume_db)
