"""Downloads the tokenizer vocabulary once, with a progress bar.

Used by tokens.py and chat_trimmed.py:
    from tokenizer_setup import get_encoding
    enc = get_encoding()

Order of preference:
  1. Already cached in .tiktoken_cache  -> instant
  2. o200k_base.tiktoken in this folder -> copied, no internet needed
  3. Otherwise                          -> downloaded once, with a progress bar

Instructor: after one successful download, run
    python tokenizer_setup.py --bundle
to create o200k_base.tiktoken, and share it with the class code.

If the connection stalls, the download pauses, reconnects and resumes
from where it stopped, instead of starting over.
"""
import hashlib
import os
import sys
import time
import urllib.error
import urllib.request

URL = "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken"
EXPECTED_SHA256 = "446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d"

HERE = os.path.dirname(os.path.abspath(__file__))
# If this file sits next to the scripts, no download is needed at all
BUNDLED_FILE = os.path.join(HERE, "o200k_base.tiktoken")

CACHE_DIR = os.path.join(HERE, ".tiktoken_cache")
# tiktoken looks for the file under the SHA-1 of its URL
CACHE_FILE = os.path.join(CACHE_DIR, hashlib.sha1(URL.encode()).hexdigest())
PART_FILE = CACHE_FILE + ".part"

MAX_ATTEMPTS = 10      # reconnect this many times before giving up
STALL_TIMEOUT = 20     # seconds with no data before we reconnect


def _progress(done, total, start, start_bytes):
    elapsed = max(time.time() - start, 0.001)
    speed = (done - start_bytes) / elapsed / 1_000_000
    if total:
        frac = done / total
        filled = int(30 * frac)
        bar = "#" * filled + "-" * (30 - filled)
        line = f"  [{bar}] {frac:6.1%}  {done/1e6:5.1f} / {total/1e6:.1f} MB  {speed:4.1f} MB/s"
    else:
        line = f"  {done/1e6:5.1f} MB downloaded  {speed:4.1f} MB/s"
    print("\r" + line + "   ", end="", flush=True)


def _download_attempt():
    """Download (or resume) into PART_FILE. Returns the total size in bytes."""
    have = os.path.getsize(PART_FILE) if os.path.exists(PART_FILE) else 0
    request = urllib.request.Request(URL)
    if have:
        request.add_header("Range", f"bytes={have}-")

    with urllib.request.urlopen(request, timeout=STALL_TIMEOUT) as response:
        if have and response.status == 206:
            # Server is resuming: "Content-Range: bytes 1100000-3613921/3613922"
            total = int(response.headers["Content-Range"].split("/")[-1])
            mode = "ab"
        else:
            # Server sent the whole file again: start over
            total = int(response.headers.get("Content-Length") or 0)
            have, mode = 0, "wb"

        if total and have >= total:
            return total

        start = time.time()
        done = have
        with open(PART_FILE, mode) as f:
            while True:
                chunk = response.read(64 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                _progress(done, total, start, have)
        return total


def _download():
    print("Downloading the tokenizer vocabulary (one time only)...")
    print(f"  from {URL}")
    os.makedirs(CACHE_DIR, exist_ok=True)
    start = time.time()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            total = _download_attempt()
            size = os.path.getsize(PART_FILE)
            if total and size < total:
                raise ConnectionError("connection closed early")
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            have = os.path.getsize(PART_FILE) if os.path.exists(PART_FILE) else 0
            if attempt == MAX_ATTEMPTS:
                print()
                raise ConnectionError(f"gave up after {MAX_ATTEMPTS} attempts ({e})")
            wait = min(2 * attempt, 10)
            print(f"\n  Connection stalled ({e}). Resuming from {have/1e6:.1f} MB "
                  f"in {wait}s (attempt {attempt + 1}/{MAX_ATTEMPTS})...")
            time.sleep(wait)
    print()

    with open(PART_FILE, "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        os.remove(PART_FILE)   # corrupted: start fresh next time
        raise ValueError("downloaded file is corrupted. Please run again.")

    os.replace(PART_FILE, CACHE_FILE)
    print(f"Done in {time.time() - start:.1f}s. Saved to {CACHE_DIR}\n")


def _sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _use_bundled_file():
    """Copy o200k_base.tiktoken from the class folder into the cache, if it's there."""
    if not os.path.exists(BUNDLED_FILE):
        return False
    if _sha256_of(BUNDLED_FILE) != EXPECTED_SHA256:
        print("Note: o200k_base.tiktoken in this folder is damaged; downloading instead.")
        return False
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(BUNDLED_FILE, "rb") as src, open(CACHE_FILE, "wb") as dst:
        dst.write(src.read())
    print("Tokenizer loaded from the class folder (no download needed).\n")
    return True


def make_bundle():
    """For the instructor: copy the downloaded file next to the scripts to share it."""
    get_encoding()
    with open(CACHE_FILE, "rb") as src, open(BUNDLED_FILE, "wb") as dst:
        dst.write(src.read())
    print(f"Created {BUNDLED_FILE}")
    print("Share this file with the class code; students won't need to download anything.")


def get_encoding():
    """Return the o200k_base tokenizer: bundled copy first, else download."""
    os.environ["TIKTOKEN_CACHE_DIR"] = CACHE_DIR
    if not os.path.exists(CACHE_FILE) and not _use_bundled_file():
        try:
            _download()
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            print(f"\nCould not download the tokenizer: {e}")
            print("Your progress is saved. Just run the script again to continue.")
            print("If it keeps failing: try another network (e.g. a phone hotspot)")
            print("or turn off your VPN.")
            sys.exit(1)

    import tiktoken
    return tiktoken.get_encoding("o200k_base")


if __name__ == "__main__":
    if "--bundle" in sys.argv:
        make_bundle()          # instructor: python tokenizer_setup.py --bundle
    else:
        enc = get_encoding()   # students:   python tokenizer_setup.py
        print("Tokenizer ready:", enc.name)
