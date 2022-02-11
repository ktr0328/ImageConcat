import os
import re
import sys
import time

import click

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from pathlib import Path
from typing import List

from dataclasses import dataclass
from loguru import logger
from natsort import natsorted
from PIL import Image
from ulid import ULID

from util.convert_non_alpha import convert
from util.worker_chunk import chunk


logger.remove()
logger.add(
    sys.stdout,
    diagnose=False,
    backtrace=False,
    level='TRACE'
)
logger.add(
    './logs/common/{time:YYYY-MM}/{time:DD}.log',
    rotation='1 day',
    diagnose=False,
    backtrace=False,
    level='INFO',
    colorize=True,
    compression='tar.gz'
)


@dataclass
class ProcPayload:
    parent_ulid: ULID
    img_dirs: List
    pdf_dir: str
    quality: int
    is_ulid: bool


def prepare(dir_path: str):
    os.makedirs(dir_path, exist_ok=True)


def convert_to_pdf(payload: ProcPayload):
    pid = os.getpid()
    logger.trace(f'{pid} task num: {len(payload.img_dirs)}.')

    convert_time = time.time()
    for d in payload.img_dirs:
        convert(Path(d), payload.quality)
    convert_elapsed = time.time() - convert_time
    logger.info(f'convert to non alpha took {convert_elapsed:.3f} sec.')

    concat_time = time.time()
    for d in payload.img_dirs:
        try:
            images_path = Path(d)
            images = natsorted([v for v in images_path.glob('*') if re.search('/*\.(jpg|jpeg|png)', str(v))])
            if len(images) == 0:
                return
            li = []
            for img in images:
                li.append(Image.open(str(img)).convert('RGB'))
            base = li[0]
            rest = li[1:]

            d_name = Path(d).stem
            filename = f'{ULID()}.pdf' if payload.is_ulid else f'{d_name}.pdf'
            pdf_file_path = Path(payload.pdf_dir, str(payload.parent_ulid), filename)
            base.save(pdf_file_path, save_all=True, append_images=rest)
            logger.success(f'{pid}:saved: {pdf_file_path}')
        except Exception as e:
            logger.error(f'{d} failed.')
    concat_elapsed = time.time() - concat_time
    logger.info(f'concat all images to each pdf took {concat_elapsed:.3f} sec.')


@click.command()
@click.argument('img_dir', type=str)
@click.option('--save_dir', type=str, default='./output/pdf')
@click.option('--ulid', type=bool, default=False)
@click.option('--quality', type=int, default=100)
def main(img_dir: str, save_dir: str, ulid: bool, quality: int):
    start_time = time.time()
    home_ulid = ULID()
    logger.info(f'image concat start @{home_ulid}.')

    prepare(save_dir)
    prepare(str(Path(save_dir, str(home_ulid))))

    worker_count = cpu_count()
    logger.trace(f'worker count: {worker_count}')
    with ProcessPoolExecutor(max_workers=worker_count) as proc:
        target_chunked = chunk(
            [Path(img_dir, v.name).resolve() for v in os.scandir(img_dir)], worker_count)

        for chunked in target_chunked:
            payload = ProcPayload(parent_ulid=home_ulid,
                                  img_dirs=chunked,
                                  pdf_dir=save_dir,
                                  quality=quality,
                                  is_ulid=ulid)
            proc.submit(convert_to_pdf, payload)

    elapsed_time = time.time() - start_time
    logger.info(f'all done took {elapsed_time:.3f} sec.')


if __name__ == '__main__':
    main()
