#!/usr/bin/python
"""Convert "Complete National Geographic" CNG files to JPG for use under Linux

cng2jpg.py --src /run/media/user/CNG_DISC1/disc1/images --dst ~/CNG/discs/images
"""

import os
import argparse
from PIL import Image

def convert_one(src_filename, dst_filename):
    """Convert source file by performing a byte-by-byte xor 239, save result into new file

    :param src_filename: source filename, will be opened read-only
    :param dst_filename: destination file, will be truncated if exists
    """
    print (dst_filename)
    with open(src_filename, 'rb') as in_stream, open(dst_filename, 'wb') as out_stream:
        out_stream.write(bytearray((c ^ 239) for c in in_stream.read()))


def convert_all(src_path, dst_path, remove=False, merge=False):
    """Recursively convert all .cng files found in src_path.

    Converted .cng files are saved as <file>.jpg under dst_path.
    Intermediary subdirectories will be created as necessary to preserve the directory structure.

    :param src_path: source directory (must exist)
    :param dst_path: target directory, can be same as source (will be created if missing)
    :param remove: if True, remove original .cng files as they are converted. Use if data was
                   already copied from CDs to local drive, to avoid needing extra 48GB of space.
    :param merge: if True, merges double spread pages into single files.
    """
    for root, dirs, files in os.walk(src_path):
        target_path = root.replace(src_path, dst_path, 1)
        for filename in files:
            basename, ext = os.path.splitext(filename)
            if ext.lower() == '.cng':
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                dst_filename = os.path.join(target_path, basename + ".jpg")
                src_filename = os.path.join(root, filename)
                convert_one(src_filename, dst_filename)
                if remove:
                    os.remove(src_filename)

            if merge:
                # Merge even-odd files in 2 page spreads
                imgnum = int(basename.split('_')[3])
                if (imgnum % 2 == 1) and (imgnum > 1):
                    rightpage_filename = dst_filename

                    basename_lst = basename.split('_')
                    basename_lst[3] = f"{imgnum-1:03}"
                    leftpage_basename = '_'.join(basename_lst)
                    leftpage_filename = os.path.join(target_path, leftpage_basename + ".jpg")

                    basename_lst = basename.split('_')
                    basename_lst[3] = f"{imgnum-1:03}-{imgnum:03}"
                    twopage_basename = '_'.join(basename_lst)
                    twopage_filename = os.path.join(target_path, twopage_basename + ".jpg")

                    # Test if left page exists, otherwise skip merge
                    if os.path.isfile(leftpage_filename):
                        print ('merge into ',dst_filename)
                        twopage = merge_images(leftpage_filename, rightpage_filename)

                        twopage.save(twopage_filename)
                        os.remove(leftpage_filename)
                        os.remove(rightpage_filename)


def merge_images(file1, file2):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    return result


def main():
    parser = argparse.ArgumentParser(description='Convert NatGeo CNG files to JPG')
    parser.add_argument('-s', '--src', required=True,
                        help='path to source directory containing files to convert')
    parser.add_argument('-d', '--dst', required=False,
                        help='optional destination path (default in-place)')
    parser.add_argument('-r', '--remove', action='store_true', default=False,
                        help='remove original cng files after conversion')
    parser.add_argument('-m', '--merge', action='store_true', default=False,
                        help='merge double spread pages in a single file')
    args = parser.parse_args()

    if args.dst and not os.path.exists(args.dst):
        os.makedirs(args.dst)

    convert_all(args.src, args.dst or args.src, remove=args.remove, merge=args.merge)


if __name__ == '__main__':
    main()
