# import libraries
import requests
import re
import argparse
# We can only use RHYMEZONE
DATAMUSE_API = "https://api.datamuse.com/words"
RHYMEZONE_API = "http://api.rhymezone.com/words?k=rza&arhy=1"


def get_ryhmes(word: str, option='rel_rhy', max=100, api_endoint="https://api.datamuse.com/words"):
    """ getting all rhyming words from the 

    Args:
        word (string): word as a string (no \n)

    Returns:
        list(str): list of words
    """
    parameter = {}
    parameter[option] = word
    parameter['max'] = max
    request = requests.get(api_endoint, parameter)
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
    sentence = sentence.replace(')', '')
    sentence = sentence.replace('(', '')
    sentence = sentence.replace('.', ' ')
    return re.split(r'\W+', sentence)[-1]


def main(filename, output_file='output.txt', nry=False):
    output = []
    i = 0
    with open(filename) as f:
        lines = f.readlines()
        lines = [line for line in lines if len(line) > 2]

        while len(lines) > 0:
            last_word = get_last_word(lines[0].strip('\n'))

            rhymes = get_ryhmes(last_word)
            output.append([])
            output[i].append(lines[0])
            lines.remove(lines[0])
            lines_swap = lines.copy()
            for s in lines_swap:
                lw = get_last_word(s.strip('\n'))
                if lw in rhymes or lw == last_word:
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
        multies = output[:separator]
        singles = output[separator:]
        mul = multies.copy()
        sin = singles.copy()
        for single in singles:
            get_out = False
            single_last_word = get_last_word(single[0].strip('\n'))

            near_rhymes = get_ryhmes(
                single_last_word, 'sl', 1000, RHYMEZONE_API)[1:]
            for i, multi in enumerate(multies):
                if not get_out:
                    for line in multi:
                        line_last_word = get_last_word(line.strip('\n'))
                        for word in near_rhymes:
                            if word == line_last_word:
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
                f.write(line + '\n'*('\n' not in line))
            f.write('\n')

    # for elt in output:
    #     print(elt)
    #     input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='rhymer.py',
        description='RhymerV0.2 script will sort sentences acording to their rhymes and near rhymes.',
        epilog='This script uses datamuse.com and  rhymezone APIs.')
    parser.add_argument('input_filename', help="Input file containing lines.")
    parser.add_argument('output_filename', default='output.txt',
                        help="output file where the sorted poem is stored.")
    parser.add_argument('-no_sl', action='store_false',
                        help="Will not use the [sl] Sound like API calls. (ie. no near rhymes)")
    args = parser.parse_args()
    try:

        main(args.input_filename, output_file=args.output_filename, nry=args.no_sl)
        print("[OK] sorted in output.txt")
    except:
        print("usage: python rhymer.py sample.txt")
