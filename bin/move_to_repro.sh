#!/bin/bash
# Helper to move a file to the git repro and replace it with a symlink
# The script is expeted to be located in the bin/ folder of the repro
set -euo pipefail

if [ "$1" == "-h" ] ; then
    echo "Move a file/directory to Linux Settings repro to keep track of it and replace it with a symlink"
    echo "Usage: `basename $0` <file to move> <folder in repro>"
    exit 0
fi

if [[ $# != 2 ]] ; then
    echo "Script requires two arguments! Use -h for help"
    exit 1
fi

# Check first parameter

if [[ ! -e "$1" ]] ; then
    echo "Selected file/directory '$1' does not exist"
    exit 1
fi

# First get the repro base
REPRO_BASE=$(dirname $(dirname $(realpath $0)))

# Check second parameter

TARGET="${REPRO_BASE}/${2}"

if [[ ! -d  $TARGET ]] ; then
    echo "There is no directory '$2' in $REPRO_BASE, create it first!"
    exit 1
fi

TARGET_FILE="${TARGET}/$(basename $1)"
SOURCE_FILE=$(realpath $1)

# Move the seleted file/dir
mv "$SOURCE_FILE" "$TARGET_FILE"

# Create reverse link
ln -s "$TARGET_FILE" "$SOURCE_FILE"
