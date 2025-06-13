# Setup Guide

## Prerequisites

- Python 3.8+
- pip
- (Optional) `mpg123` or `ffmpeg` for audio playback

## Installation

1. Clone the repository and navigate to the folder.

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install requirements:
    ```bash
    pip install --upgrade pip
    pip install --no-cache-dir -r multiagent_support/requirements.txt
    ```

4. (Optional) Install system audio tools:
    ```bash
    sudo apt-get install mpg123 ffmpeg  # Ubuntu/Debian
    sudo pacman -S mpg123 ffmpeg        # Arch
    ```

## Running the API

```bash
uvicorn multiagent_support.api:app --reload
```
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive docs.

## Running the CLI

```bash
python -m multiagent_support.cli
```

---