import asyncio
import aiofiles
import os
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_path, output_path):
    try:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                await copy_file(file_path, output_path)
                logging.info(f'File {file} read from {root}')
    except Exception as e:
        logging.error(f'Error reading folder {source_path}: {e}')


async def copy_file(file_path, output_path):
    try:
        extension = os.path.splitext(file_path)[1][1:] or 'NoExtension'
        dest_folder = os.path.join(output_path, extension)
        os.makedirs(dest_folder, exist_ok=True)
        dest_file = os.path.join(dest_folder, os.path.basename(file_path))
        async with aiofiles.open(file_path, 'rb') as src, aiofiles.open(dest_file, 'wb') as dst:
            await dst.write(await src.read())
        logging.info(f'File {os.path.basename(file_path)} copied to {dest_folder}')
    except Exception as e:
        logging.error(f'Error copying file {file_path}: {e}')


def setup_args():
    parser = argparse.ArgumentParser(description="Sort files based on their extensions asynchronously.")
    parser.add_argument('--source', help="Path to the read folder")
    parser.add_argument('--output', help="Path to the copy folder")
    args = parser.parse_args()

    if not args.source:
        args.source = input("Enter the path to the read folder: ")
    if not args.output:
        args.output = input("Enter the path to the copy folder: ")

    return args


async def main():
    args = setup_args()
    await read_folder(args.source, args.output)


if __name__ == '__main__':
    asyncio.run(main())
