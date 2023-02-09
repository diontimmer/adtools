import os
import argparse
import glob
from pydub import AudioSegment
from tqdm import tqdm

def cut_audio_files(dir_path, chunk_length_samples, sample_rate, output_folder):
    # Get a list of all the WAV files in the directory (recursively)
    wav_files = glob.glob(os.path.join(dir_path, "**", "*.wav"), recursive=True)

    # Loop over all files in the list
    prog = tqdm(wav_files)
    for file_path in prog:
        file_name = os.path.basename(file_path)

        # Load the audio file
        audio = AudioSegment.from_file(file_path, format="wav")

        # Calculate the length of the audio file in milliseconds
        audio_length_ms = len(audio)
        
        # Calculate the length of the audio file in samples
        audio_length_samples = audio_length_ms * sample_rate / 1000

        # Calculate the length of each chunk in milliseconds
        chunk_length_ms = chunk_length_samples * 1000 / sample_rate

        # Calculate the number of chunks
        num_chunks = int(audio_length_samples // chunk_length_samples)

        # Iterate over each chunk
        prog.set_description(f'Cutting {file_name} into {num_chunks} chunks.')
        for i in range(num_chunks):
            chunk_start = i * chunk_length_ms
            chunk_end = (i + 1) * chunk_length_ms

            # Extract the chunk
            chunk = audio[chunk_start:chunk_end]

            # Save the chunk as a separate file
            chunk.export(os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_chunk_{i}.wav"), format="wav")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut audio files into chunks")
    parser.add_argument("dir_path", type=str, help="Path to the directory containing the audio files")
    parser.add_argument("chunk_length_samples", type=int, help="Length of each chunk in samples")
    parser.add_argument("sample_rate", type=int, help="Sample rate of the audio files in samples per second")
    parser.add_argument("output_folder", type=str, help="Path to the directory where the cut chunks will be saved")
    args = parser.parse_args()
    cut_audio_files(args.dir_path, args.chunk_length_samples, args.sample_rate, args.output_folder)
