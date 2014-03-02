#!/usr/bin/env python

"""
less-prefixed.py

Chains less and autoprefixer, to produce a minified, vendor-prefixed css file.
"""

# TODO: move config data to a config file

import argparse
import os
import subprocess
from pprint import pprint as pp

# Config data
node_folder = r'C:/Users/VadShaytReth/AppData/Roaming/npm'
less_script = os.path.join(node_folder, 'lessc.cmd')
autoprefixer_script = os.path.join(node_folder, 'autoprefixer.cmd')

parser = argparse.ArgumentParser()
parser.add_argument("--file-name", help="filename, not including the extension", required=True)
parser.add_argument("--working-dir", help="the directory to do the work in", required=True)
args = parser.parse_args()

print('\nArgs:')
pp(vars(args))
print('')

os.chdir(args.working_dir)
print('CWD: {c}\n'.format(c=os.getcwd() + '\n'))

print('Running less-css...')

# Compile and minify the less file to css.
# Include a sourcemap.
exitcode = subprocess.Popen([
    less_script,
    '--no-color',
    '-x',
    '--source-map={n}.css.map'.format(n=args.file_name),
    '{n}.less'.format(n=args.file_name),  # source
    '{n}.min.css'.format(n=args.file_name)  # dest
], cwd=args.working_dir).wait()

assert exitcode is 0, 'Nonzero return code from less! Got: {r}'.format(r=exitcode)
print('less compilation completed.\nRunning autoprefixer...')

# Run autoprefixer over the result from lessc.
exitcode = subprocess.Popen([
    autoprefixer_script,
    '-o',
    '{n}.prefixed.min.css'.format(n=args.file_name),  # dest
    '{n}.min.css'.format(n=args.file_name)  # source
], cwd=args.working_dir).wait()

assert exitcode is 0, 'Nonzero return code from autoprefixer! Got: {r}'.format(r=exitcode)

print('autoprefixer completed.\nFinal filename is {n}.prefixed.min.css'.format(n=args.file_name))