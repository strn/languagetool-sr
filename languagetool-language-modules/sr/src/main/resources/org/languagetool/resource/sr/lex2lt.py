#!/usr/bin/env python3
# coding: utf-8

# Program transforms Serbian word corpus into number of files.
# Each file has structure similar to main word corpus file
# with some differences:
#
# 1. Words in Latin alphabet are transliterated into Cyrillic
# 2. Each word is stored in file <XX>-words.txt, where <XX> is
# Latin equivalent of Cyrillic letters

import argparse
import logging
import re
import os
import sys

"""
Program reads morphologic dictionary from a single file, line by line, splitting entries into
multiple files. File where each line will go is determined by first letter of lemma. Example:

If lemma == "apple", then whole line goes to file "a-words.txt" etc.

If entries are in Croatian Latin script, they are converted into Serbian Cyrillic script.
"""

_args_ = None
_logger_ = None
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
CYR_LETTERS = {
    'а' : 'a',
    'б' : 'be',
    'в' : 've',
    'г' : 'ge',
    'д' : 'de',
    'ђ' : 'dje',
    'е' : 'e',
    'ж' : 'zhe',
    'з' : 'ze',
    'и' : 'i',
    'ј' : 'je',
    'к' : 'ka',
    'л' : 'lamda',
    'љ' : 'lje',
    'м' : 'em',
    'н' : 'en',
    'њ' : 'nje',
    'о' : 'o',
    'п' : 'pe',
    'р' : 'er',
    'с' : 'es',
    'т' : 'te',
    'ћ' : 'tshe',
    'у' : 'u',
    'ф' : 'ef',
    'х' : 'ha',
    'ц' : 'ce',
    'ч' : 'ch',
    'џ' : 'dzhe',
    'ш' : 'sha',
    'misc' : 'misc', # For miscellaneous "words"
    'unmatched' : 'unmatched'
}

# Types of regex to match input, selectable from command line
REGEX_TYPE = {
    "lex" : "^([!\"\'\(\),\-\.:;\?]|[a-zčćžšđâîôﬂǌüöäø’A-ZČĆŽŠĐ0-9_\-]+)\s+([!\"\'\(\),\-\.:;\?]|[a-zčćžšđâîôﬂǌüöäø’A-ZČĆŽŠĐ0-9_\-]+)\s+([a-zA-Z0-9\-]+)\s+(\d+)*",
    "wac" : "^([a-zčćžšđâîôﬂǌüöäø’A-ZČĆŽŠĐ0-9_\-]+)\s+([!\"\'\(\),\-\.:;\?]|[a-zčćžšđâîôﬂǌüø’A-ZČĆŽŠĐ0-9_\-]+)\s+([!\"\'\(\),\-\.:;\?]|[a-zčćžšđâîôﬂǌüöäø’A-ZČĆŽŠĐ0-9_\-]+)\s+([a-zA-Z0-9\-]+)\s+(\d+)*"
}

# Map holding transliterated Cyrillic letters pointing to
# descriptors of opened files
WORD_FILES = {}

LAT_LIST = (u"Đ", u"Dž", u"DŽ", u"LJ", u"Lj", u"NJ", u"Nj", u"A", u"B", u"V", u"G", u"D", u"E", u"Ž", u"Z", u"I", u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"R", u"S", u"T", u"Ć", u"U", u"F", u"H", u"C", u"Č", u"Š", u"a", u"b", u"v", u"g", u"dž", u"d", u"e", u"ž", u"z", u"i", u"j", u"k", u"lj", u"l", u"m", u"nj", u"n", u"o", u"p", u"r", u"s", u"t", u"ć", u"u", u"f", u"h", u"c", u"č", u"š", u"đ", u"Ð", u"ǌ", u"ﬂ" )

CIR_UTF_LIST = (u"Ђ", u"Џ", u"Џ", u"Љ", u"Љ", u"Њ", u"Њ", u"А", u"Б", u"В", u"Г", u"Д", u"Е", u"Ж", u"З", u"И", u"Ј", u"К", u"Л", u"М", u"Н", u"О", u"П", u"Р", u"С", u"Т", u"Ћ", u"У", u"Ф", u"Х", u"Ц", u"Ч", u"Ш", u"а", u"б", u"в", u"г", u"џ", u"д", u"е", u"ж", u"з", u"и", u"ј", u"к", u"љ", u"л", u"м", u"њ", u"н", u"о", u"п", u"р", u"с", u"т", u"ћ", u"у", u"ф", u"х", u"ц", u"ч", u"ш", u"ђ", u"Ђ", u"њ", u"фл" )

def parse_args():
    parser = argparse.ArgumentParser(description='Processes file containing Serbian word corpus.')
    parser.add_argument('-b', '--base-dir',   default='/tmp')
    parser.add_argument('-d', '--debug',      action ='store_true', default=False)
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-n', '--first-n-lines', default=0, type=int)
    parser.add_argument('-r', '--regex',      default=None)
    global _args_, _logger_
    _args_ = parser.parse_args()
    if _args_.debug:
        _logger_.setLevel( logging.DEBUG )
    else:
        _logger_.setLevel( logging.INFO )
    _logger_.debug( "Command-line arguments: {}".format(_args_) )
    if not _args_.input_file:
        _logger_.error("Input file was not specified, aborting ...")
        sys.exit(1)
    if not _args_.regex:
        sys.exit(1)
    if not os.path.exists(_args_.input_file):
        _logger_.error("Unable to open file '{}', aborting ...".format(_args_.input_file))
        sys.exit(1)


# Open files for writing words in directory specified with "-b" option
# Files are opened in append mode
def open_out_files():
    global WORD_FILES
    for cl, lett in CYR_LETTERS.items():
        out_dir = os.path.join(_args_.base_dir, lett)
        if not os.path.exists( out_dir ):
            os.makedirs( out_dir )
        WORD_FILES[ cl ] = list()
        _logger_.debug( "Opening file {}/{}-words.txt ...".format(out_dir, lett) )
        WORD_FILES[ cl ].append( open( os.path.join(out_dir, lett + '-words.txt'), 'wb+' ) )
        _logger_.debug( "Opening file {}/{}-names.txt ...".format(out_dir, lett) )
        WORD_FILES[ cl ].append( open( os.path.join(out_dir, lett + '-names.txt'), 'wb+' ) )


# Close all files containing words
def close_out_files():
    for cl, lett_files in WORD_FILES.items():
        _logger_.debug('Closing file {}-words.txt ...'.format(CYR_LETTERS[ cl ]))
        lett_files[0].close()
        _logger_.debug('Closing file {}-names.txt ...'.format(CYR_LETTERS[ cl ].upper()))
        lett_files[1].close()


def init():
    global _logger_
    logging.basicConfig(format=LOG_FORMAT)
    _logger_ = logging.getLogger("lex2lt")


# Determine output file for word tripple
# based on first letter of lemma
def get_words_out_file( first_char ):
    if first_char.lower() in WORD_FILES:
        # Is this really lower case?
        if first_char == first_char.lower():
            out_file = WORD_FILES[ first_char.lower() ][0]
        else:
            out_file = WORD_FILES[ first_char.lower() ][1]
    else:
        out_file = WORD_FILES[ 'misc' ][0]
    return out_file


# Parse input file
def parse_file():
    cnt = 0
    matchcnt = 0
    if _args_.regex in REGEX_TYPE:
        pattern = re.compile(REGEX_TYPE[ _args_.regex ])
    else:
        _logger_.error("Regular expression of type '{}' does not exist in configuration, aborting ...".format(_args_.regex))
        sys.exit(1)
    # Create conversion dictionary for Latin to Cyrillic conversion
    conv_dict = dict(zip(LAT_LIST, CIR_UTF_LIST))
    _logger_.debug("Conversion dictionary Lat/Cir: {}".format(conv_dict))
    comp_dict = re.compile('|'.join(conv_dict))
    _logger_.info("Started processing input file '{}' ...".format(_args_.input_file))

    with open(_args_.input_file) as f:
        for line in f:
            # Remove end of line
            line = line.strip()
            cnt += 1
            tokens = line.split('\t')
            if len(tokens) == 5:
                matchcnt += 1
                flexform = tokens[0]
                lemma = tokens[1]
                posgr = tokens[2]
                frequency = tokens[3]
                _logger_.debug(
                    'flexform={}, lemma={}, posgr={}, frequency={}'.format(flexform, lemma, posgr, frequency))
                # Transliterate flexform and lemma
                conv_flex_form = comp_dict.sub(lambda m:conv_dict[m.group()], flexform)
                conv_lemma = comp_dict.sub(lambda m:conv_dict[m.group()], lemma)
                _logger_.debug('Converted flexform={}, lemma={}'.format(conv_flex_form, conv_lemma))
                # Determine file to write line in ...
                out_file = get_words_out_file(conv_lemma[0])
                # Create line for writing in file
                out_file.write("{}\t{}\t{}\t{}\n".format(
                    conv_flex_form, conv_lemma, posgr, frequency).encode('utf-8'))
            else:
                _logger_.warn("Unmatched line: {}".format(line))
                out_file = WORD_FILES[ 'unmatched' ][0]
                # We will split line simply based on TAB char and write first four tokens
                tokens = line.split('\t')
                if len(tokens) == 1:
                    out_file.write("{}\n".format(tokens[0]).encode('utf-8'))
                elif len(tokens) == 2:
                    out_file.write("{}\t{}\n".format(tokens[0], tokens[1]).encode('utf-8'))
                elif len(tokens) == 3:
                    out_file.write("{}\t{}\t{}\n".format(tokens[0], tokens[1], tokens[2]).encode('utf-8'))
                elif len(tokens) == 4:
                    out_file.write("{}\t{}\t{}\t{}\n".format(tokens[0], tokens[1], tokens[2], tokens[3]).encode('utf-8'))
            if cnt > _args_.first_n_lines > 0:
                break
        f.close()
    _logger_.info("Finished processing input file '{}': total {} lines, {} matching lines.".format(_args_.input_file, cnt, matchcnt))


if __name__ == "__main__":
    init()
    parse_args()
    open_out_files()
    parse_file()
    close_out_files()