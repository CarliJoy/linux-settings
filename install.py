#!/usr/bin/env python3
"""
Create symlinks in your home directory for each file in this repository
starting with an undersore (which will be replaced by a dot).

If a destination file already exists, create a backup first.

based on: https://gitlab.com/sscherfke/dotfiles
"""
import os
import pathlib
import time
import functools
from typing import Optional

HOME = pathlib.Path.home()
HERE = pathlib.Path(__file__).parent.resolve()

DOT_FILE = HERE / "settings"


@functools.lru_cache(maxsize=1)
def get_bak_suffix() -> str:
    return time.strftime("%Y%m%d%H%M%S")


def create_link(orignal_file: pathlib.Path, dest: pathlib.Path):
    src = orignal_file
    if dest.exists():
        if dest.is_symlink() and dest.resolve() == src:
            print(f"{dest} is already a correct link")
            return

        bak = dest.with_name(f"{dest.name}.{get_bak_suffix()}")
        print(f"Backing up {dest} -> {bak}")
        dest.rename(bak)
    if dest.is_symlink() and not dest.exists():
        dest.unlink()  # Remove broken symlinks

    print(f"Linking {src} -> {dest}")
    os.symlink(src, dest)


def create_home_links(relative_path: Optional[pathlib.Path] = None):
    """
    Recursively create setting files in home
    """
    if relative_path is None:
        repro_path = DOT_FILE
    else:
        repro_path = DOT_FILE / relative_path
    for elm in repro_path.iterdir():
        new_realtiv = elm.relative_to(DOT_FILE)
        home_target = HOME / new_realtiv
        if elm.is_dir():
            if home_target.exists() and not home_target.is_dir():
                print(f"Error: Expected '{home_target}' to be a directory!")
                continue
            home_target.mkdir(exist_ok=True)
            create_home_links(new_realtiv)
        else:
            create_link(elm, home_target)


def main():
    """Install/link config files."""
    create_home_links()

    #HOME.joinpath(".local", "bin").mkdir(parents=True, exist_ok=True)
    #HOME.joinpath(".ssh").mkdir(mode=0o700, exist_ok=True)
    #for f in HOME.joinpath(".ssh").iterdir():
    #    f.chmod(0o600)


if __name__ == "__main__":
    main()

