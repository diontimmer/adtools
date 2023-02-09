import argparse
import os
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib.parse

audio_formats = {".wav", ".mp3", ".ogg", ".m4a"}

def download_audio(session, href, url, output_dir, prog):
    audio_url = url + href
    try:
        audio_response = session.get(audio_url)
    except:
        print(f'Connection error for {audio_url}')
        return
    output_path = os.path.join(output_dir, urllib.parse.unquote(href))
    with open(output_path, "wb") as f:
        f.write(audio_response.content)
    prog.update(1)


def download_all_audio(session, url, output_dir, max_workers=5, non_recursive=False):
    print(f'Downloading from {url} to {output_dir}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        response = session.get(url)
    except:
        print(f'Connection error for {url}')
        return
    soup = BeautifulSoup(response.content, "html.parser")
    raw_links = soup.find_all("a")
    audio_links = [link for link in raw_links if link.get("href").endswith(tuple(audio_formats))]
    dir_links = [link for link in raw_links if link.get("href").endswith("/")]
    dir_links = [link.get("href") for link in dir_links]
    for link in dir_links:
        if link in url:
            dir_links.remove(link)
    dir_links = list(dict.fromkeys(dir_links))
    dir_links = [url + link for link in dir_links]

    # process

    if audio_links:
        prog = tqdm(total=len(audio_links), initial=0)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for link in audio_links:
                href = link.get("href")
                executor.submit(download_audio, session, href, url, output_dir, prog)
        prog.close()
    else:
        print('No audio files found.')
    print(f'Directory complete!\n')

    # recursive

    if not non_recursive:
        for directory in dir_links:
            nw_out = urllib.parse.unquote(os.path.join(output_dir + '/' + directory.split('/')[-2]))
            download_all_audio(session, directory, nw_out, max_workers, non_recursive)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download all audio files from an open HTTP directory.')
    parser.add_argument('url', help='URL of the directory to download from')
    parser.add_argument('output_dir', nargs='?', type=str, default=None, help='Output directory to save the audio files to')
    parser.add_argument('--max-workers', type=int, default=20, help='Maximum number of concurrent workers')
    parser.add_argument('--non_recursive', action='store_true', help='Download files from only the current directory')
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = urllib.parse.unquote(os.path.join(os.getcwd(), args.url.split('/')[-2]))
        print(args.output_dir)
        breakpoint()

    print('Starting session.')
    session = requests.Session()

    download_all_audio(session, args.url, args.output_dir, args.max_workers, args.non_recursive)
    print('Script complete!')
