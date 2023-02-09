# adtools
 Personal Python scripts for audio diffusion

 # splice.py - Splice up audio files to set chunk length<br>
 
 ```
usage: splice.py [-h] dir_path chunk_length_samples sample_rate output_folder

positional arguments:
  dir_path              Path to the directory containing the audio files
  chunk_length_samples  Length of each chunk in samples
  sample_rate           Sample rate of the audio files in samples per second
  output_folder         Path to the directory where the cut chunks will be saved
  ```
  
 # sf2_export.py - Export soundfont files to wave<br>
 ```
usage: sf2_export.py [-h] [--raw] soundfont_path output_folder

positional arguments:
  soundfont_path  Path to the soundfont file
  output_folder   Output folder to save the WAV files
  
options:
  --raw           Do not normalize the audio files
```
