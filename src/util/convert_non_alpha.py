import os

from pathlib import Path

from PIL import Image


def convert(img_dir: Path, quality: int, logger):
    pid = os.getpid()
    files = img_dir.glob('*.png')

    for file in files:
        im = Image.open(file)
        im = im.convert('RGB')
        new_file = file.parent / (file.stem + '.jpeg')
        im.save(new_file, quality=quality)
        file.unlink()
        logger.trace(f'{pid}:convert to non_alpha: {new_file.resolve()}')
