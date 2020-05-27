#!/usr/bin/env python3
"""Structurize flat collection of photos based on structured miniatures.

Use handy miniatures to manually sort the photos, then, prepare set for
 delivery by adding structure to flat, high-quality images or videos.

Author: Krystian Safjan
License: MIT

Workflow
- directory for each event
- for each event create sel subdir
- copy all photos of the event to dedicated folder
- manually move image of interest ("selected") to sel subdir of event
- keep the unselected photos in event dir

Usage examples:
mimi.py prev_dir hq_flat_dir hq_struct_dir

Options:
Let's assume we have structure:
01_waterfalls/
    sel/
        img_1.jpg
        img_2.jpg

'--sel-only', '-s'
    Keep only content of "sel" subdirectories

'--level-up-sel', '-l'
    Move content of sel folder

'--move-to-top-level', '-t',
    Move contents of all sel folders to top level

'--add-prefix', '-p'
    Add event directory as filename prefix

'--verbose', '-v',
    Display more information on what is happening during the operation.

'--force', '-f',
    Force removing of the output directory if exists.

TODO:
- add support for other than "sel" names of sel* folder, use regex instead of {pattern}{sep}
"""
import argparse
import logging
import os
import pathlib
import shutil
from typing import List

logging.basicConfig(level=logging.INFO)


def ignore_files(directory, files) -> list:
    """Callable that returns list of files to be ignored while copying tree.

    Ignore files
    """

    return [f for f in files if os.path.isfile(os.path.join(directory, f))]


def copy_tree(input_path: str, output_path: str, force: bool, move_to_top_level):
    """Copy structure of input path excluding files."""
    logging.debug('Starting copy procedure for directory structure.')
    if os.path.isdir(output_path):
        if force:
            logging.warning(
                f'Output directory {output_path} exists. Removing since force option was used.')
            shutil.rmtree(output_path)
        else:
            logging.error('Output directory exists. Aborting.')
            exit(1)

    if not move_to_top_level:
        shutil.copytree(input_path, output_path, ignore=ignore_files)
        logging.debug(f'copied structure from:{input_path} to: {output_path}')
    else:
        os.makedirs(output_path)


def list_dir(root_dir: str) -> List[str]:
    """Return list of files in given path (recursive)."""
    file_list = []
    logging.debug('Getting list of files in original structure.')
    for current_path, folders, files in os.walk(root_dir):
        for file in files:
            full_file = os.path.join(current_path, file)
            if not file.startswith('.'):
                logging.debug(full_file)
                file_list.append(full_file)
            else:
                logging.debug(f'Skipping: {full_file}')
    return file_list


def copy_files(input_HD_files: List[str],
               input_prev_files: List[str],
               output_files: List[str]):
    """Copy files from one list to targets defined in second list

    :param input_prev_files:
    :param input_HD_files:
    :param input_files:
    :param output_files:
    :return:
    """
    logging.debug('Copying HQ files from flat dir to structured dir.')
    cnt = 0
    err = 0
    wrn = 0
    for src_hd, src_prev, dst in zip(input_HD_files, input_prev_files, output_files):
        try:
            shutil.copyfile(src_hd, dst)
            cnt += 1
        except FileNotFoundError:
            print(f'WRN: {src_prev}\t{src_hd}')
            wrn += 1
            try:
                shutil.copyfile(src_prev, dst)
            except FileNotFoundError:
                print(f'ERR: {src_prev}\t{src_hd}')
                err += 1
    logging.info(f'Copied {cnt} files. WRN: {wrn}, ERR: {err}')


def keep_sel_only(input_files: List[str], pattern: str = 'sel'):
    """Remove targets that are not is subdirs considered as selected photos.

    :param input_files:
    :param pattern:
    :return:
    """
    logging.debug('Removing targets that are not in selected folders.')
    sep = os.path.sep
    filtered_input_files = [
        f for f in input_files if f'{sep}{pattern}{sep}' in f
    ]
    logging.debug(f'Removed {len(input_files) - len(filtered_input_files)} targets.')
    return filtered_input_files


def level_up_sel_targets(output_files, pattern: str = 'sel'):
    logging.debug('Converting targets to put content of selected folders one level up.')
    sep = os.path.sep
    filtered_output_files = [
        f.replace(f'{sep}{pattern}{sep}', sep) for f in output_files
    ]
    return filtered_output_files


def add_parent_dir_prefix(output_files, add_prefix, move_to_top_level):
    logging.debug('Adding parent dir prefix to filename')
    sep = os.path.sep
    prefixed_output_files = []
    for file_path in output_files:
        pth, file = os.path.split(file_path)
        parent = str(pth).split(sep)[-1]

        if add_prefix:
            file_new = '__'.join([parent, file])
        else:
            file_new = file

        if move_to_top_level:
            p = pathlib.Path(file_path)
            path = p.parents[1]
        else:
            path = pth
        full_file = os.path.join(path, file_new)

        prefixed_output_files.append(full_file)
    return prefixed_output_files


def correct_target_path(input_files, dir_before, dir_after):
    """Replace previews path with output path in list of input preview files.

    :param input_files:
    :param dir_before:
    :param dir_after:
    :return:
    """

    # enforce trailing slash
    dir_before = os.path.join(dir_before, '')
    dir_after = os.path.join(dir_after, '')

    logging.debug(f'replacing in target path {dir_before} with {dir_after}')
    output_files = [full_file.replace(dir_before, dir_after)
                    for full_file in input_files]
    return output_files


def prepare_sources(input_prev_files: List[str], flat_hq_dir: str):
    logging.debug('Preparing sources - list of files from flat dir with HQ photos')
    src = []
    for f in input_prev_files:
        f_orig = os.path.split(f)[1]
        f_orig_raw = f_orig[5:]  # FIXME: KS: 2020-02-28: Use regular expression here
        src.append(os.path.join(flat_hq_dir, f_orig_raw))
    return src


def remove_sel_target_dirs(input_files_sel, pattern='sel'):
    sep = os.path.sep
    logging.debug(
        f'Removing selected directories from target structure since level-up option was used.')
    input_dirs_all = [os.path.split(f)[0] for f in input_files_sel]
    input_dirs_uniq = list(set(input_dirs_all))
    input_dirs_uniq_sel = [d for d in input_dirs_uniq if f'{sep}{pattern}' in d]
    for sel_directory in input_dirs_uniq_sel:
        logging.debug(f'removing {sel_directory}')
        try:
            os.rmdir(sel_directory)
        except Exception as ex:
            print(ex)


def main(args):
    # create empty structure of directories
    copy_tree(args.prev_dir, args.hq_struct_dir, args.force, args.move_to_top_level)

    # discover files to copy in previews
    in_prev_files = list_dir(args.prev_dir)

    # keep sel only
    in_files_sel = in_prev_files
    if args.sel_only:
        in_files_sel = keep_sel_only(in_prev_files)

    # prepare targets (replace prev_dir with output_dir)
    targets = correct_target_path(input_files=in_files_sel,
                                  dir_before=args.prev_dir,
                                  dir_after=args.hq_struct_dir)

    # prepare HQ sources
    # TODO: KS: 2019-12-26: handle non-existing sources
    sources = prepare_sources(
        input_prev_files=in_files_sel,
        flat_hq_dir=args.hq_flat_dir)

    # level-up selections
    out_files_level_up = targets
    if args.sel_only and args.level_up_sel:
        out_files_level_up = level_up_sel_targets(targets)
        if not args.move_to_top_level:
            remove_sel_target_dirs(targets)


    out_files_level_up = add_parent_dir_prefix(out_files_level_up, args.add_prefix,
                                               args.move_to_top_level)

    # finally, copy the high quality
    copy_files(sources, in_files_sel, out_files_level_up)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Copy directory tree with replacing previews with hi-quality images")
    # positional arguments
    parser.add_argument('prev_dir',
                        help="Directory with previews structurized into subdirectories")
    parser.add_argument('hq_flat_dir',
                        help="Directory with multimedia in high quality, flat structure")
    parser.add_argument('hq_struct_dir',
                        help="Directory with multimedia in high quality, with mirrored structure")

    parser.add_argument('--sel-only', '-s', action='store_true',
                        help='Keep only content of "sel" subdirectories')
    parser.add_argument('--level-up-sel', '-l', action='store_true',
                        help='Move content of sel folder')
    parser.add_argument('--move-to-top-level', '-t', action='store_true',
                        help='Move contents of all sel folders to top level')
    parser.add_argument('--add-prefix', '-p', action='store_true',
                        help='add event directory as filename prefix')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Display more information on what is happening during the operation.')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force removing of the output directory if exists.')

    arguments = parser.parse_args()

    main(arguments)
