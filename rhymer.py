# import libraries
import requests
import re
import sys

def get_ryhmes(word:str):
    """ getting all rhyming words from the API

    Args:
        word (string): word as a string (no \n)

    Returns:
        list(str): list of words
    """
    parameter = {}
    parameter['rel_rhy'] = word
    request = requests.get('https://api.datamuse.com/words', parameter)
    print(f"chekcing rhymes for {word}...")
    rhyme = request.json()
    return [elt['word'] for elt in rhyme]

# getting all ryhmes from api.datamuse.com
def last_word(sentence: str):
    """getting last word of a sentence

    Args:
        sentence (str): _description_

    Returns:
        _type_: _description_
    """
    return re.split(r'\W+', sentence)[-1]


def main(filename):
    output = []
    i = 0
    with open(filename) as f:
        lines = f.readlines()
        while len(lines) > 0:

            rhymes = get_ryhmes(last_word(lines[0].strip('\n')))
            output.append([])
            output[i].append(lines[0])
            lines.remove(lines[0])
            lines_swap = lines.copy()
            for s in lines_swap:
                if last_word(s.strip('\n')) in rhymes:
                    lines.remove(s)
                    output[i].append(s)

            i += 1
    #sorting based on number of rhyming sentences 
    output.sort(key=len, reverse=True)
    with open('output.txt', 'w') as f:
        for lines in output:
            for line in lines:
                f.write(line)
            f.write('\n')


try:
    main(sys.argv[1])
    print("[OK] sorted in output.txt")
except:
    print("usage: python rhymer.py sample.txt")
