# Font Anti-Aliasing & Sharpening Tool

Automatically improves quality of fonts and icons (PNG, JPG, ICO) using super-sampling + Lanczos downscaling.

Perfect for old game fonts, UI icons, logos with transparency.

### Features
- Sharpens edges
- Smooths anti-aliasing
- Removes blur and halo around letters
- Preserves transparency and original size

## Requirements
- Python 3.8+
- Pillow

## Installation

### Clone the repository
```bash
git clone https://github.com/quinsaiz/image-improver.git
cd image-improver
```

### Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### Install the requirements
```bash
pip install -r requirements.txt
```
## Usage

1. Place your files (PNG, JPG, JPEG, ICO) in the same folder as the script

2. Run
    ```bash
    python main.py
    ```

3. Enhanced files appear in the `output` folder

### Tip

For very noisy fonts try scale_factor=6 (slower but cleaner).