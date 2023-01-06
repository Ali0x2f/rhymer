# import libraries
import request
import re
import sys
import argparse


def get_ryhmes(word: str, option='rel_rhy', max=100):
    """ getting all rhyming words from the API

    Args:
        word (string): word as a string (no \n)

    Returns:
        list(str): list of words
    """
    parameter = {}
    parameter[option] = word
    parameter['max'] = max
    request = request.get('https://api.datamuse.com/words', parameter)
    print(f"checking [{option}] for {word}...")
    rhyme = request.json()
    return [elt['word'] for elt in rhyme]

# getting all ryhmes from api.datamuse.com


def get_last_word(sentence: str):
    """getting last word of a sentence

    Args:
        sentence (str): _description_

    Returns:
        _type_: _description_
    """
    return re.split(r'\W+', sentence)[-1]


def main(filename, output_file='output.txt', nry=False):
    output = []
    i = 0
    with open(filename) as f:
        lines = f.readlines()
        while len(lines) > 0:

            rhymes = get_ryhmes(get_last_word(lines[0].strip('\n')))
            output.append([])
            output[i].append(lines[0])
            lines.remove(lines[0])
            lines_swap = lines.copy()
            for s in lines_swap:
                if get_last_word(s.strip('\n')) in rhymes:
                    lines.remove(s)
                    output[i].append(s)

            i += 1
    # sorting based on number of rhyming sentences
    output.sort(key=len, reverse=True)
    # output has lines

    # near rhymes section
    if nry:
        print("[INFO] checking near rhymes.")
        separator = 0
        for separator, elt in enumerate(output):
            if len(elt) == 1:
                break
        multies = output[:separator-1]
        singles = output[separator:]
        mul = multies.copy()
        sin = singles.copy()
        for single in singles:
            get_out = False
            single_last_word = get_last_word(single[0].strip('\n'))

            near_rhymes = get_ryhmes(single_last_word, 'sl', 1000)
            for i, multi in enumerate(multies):
                if not get_out:
                    for line in multi:
                        line_last_word = get_last_word(line.strip('\n'))
                        for word in near_rhymes:
                            if word.endswith(line_last_word):
                                mul[i].append(single[0])
                                sin.remove(single)
                                get_out = True
                                break
                        else:
                            continue
                        break
                else:
                    break
        output = mul + sin
        output.sort(key=len, reverse=True)
        
        
    # output part
    with open(output_file, 'w') as f:
        for lines in output:
            for line in lines:
                f.write(line)
            f.write('\n'*2)

    # for elt in output:
    #     print(elt)
    #     input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'rhymer.py',
                    description = 'RhymerV0.2 script will sort sentences acording to their rhymes and near rhymes.',
                    epilog = 'This script uses datamuse.com API.')
    parser.add_argument('input_filename', help="Input file containing lines.")
    parser.add_argument('output_filename',default='output.txt', help="output file where the sorted poem is stored.")
    parser.add_argument('-no_sl', action='store_false', help="Will not use the [sl] Sound like API calls. (ie. no near rhymes)")
    args = parser.parse_args()
    try:
        
        main(args.input_filename,output_file=args.output_filename, nry=args.no_sl)
        print("[OK] sorted in output.txt")
    except:
        print("usage: python rhymer.py sample.txt")
