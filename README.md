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

 # dir_dl.py - Download all audio files from an open HTTP directory<br>
 ```
usage: dir_dl.py [-h] [--max-workers MAX_WORKERS] [--non_recursive] url [output_dir]

Download all audio files from an open HTTP directory.

positional arguments:
  url                   URL of the directory to download from
  output_dir            Output directory to save the audio files to

options:
  -h, --help            show this help message and exit  
  --max-workers         Maximum number of concurrent workers
  --non_recursive       Download files from only the current directory
  ```