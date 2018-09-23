from sys import argv
from networkx import DiGraph, topological_sort


def restore_alphabet(input_file_path=None):
    """
    This function restores the original alphabet from given dictionary.
    Here dictionary is considered as passed in txt-file.
    Commands:
        python main.py - simple test, which shows result via console
        python main.py /tmp/alphabet.txt - run script with data from
            specific file. Results are put in 'result.txt'.
    :param input_file_path: file with dictionary.
    :return: list of chars, which are considered to be the wanted alphabet
    """
    with open(input_file_path, 'r') as dictionary:
        dg = DiGraph()
        
        # get first word
        previous_word = dictionary.readline()
        previous_word = previous_word.strip()
        previous_position = 1
        dg.add_nodes_from(previous_word)
        
        # get second word, if it is one
        current_word = dictionary.readline()
        while current_word:
            current_word = current_word.strip()
            current_position = previous_position + 1
            
            # look for the first non-equal chars,
            # which are situated on the same positions in
            # previous word and current word
            index = 0
            length_previous = len(previous_word)
            length_current = len(current_word)
            
            while (index < length_previous and
                   index < length_current):
                if previous_word[index] == current_word[index]:
                    index += 1
                else:
                    # if the pair is found, and there is no opposite rule of
                    # any kind, add chars as nodes and an edge,
                    # which demonstrates their order.
                    if dg.has_edge(current_word[index], previous_word[index]):
                        raise Exception(
                            "Wrong words order!\n"
                            "This pair of words violates rule: {} -> {}.\n"
                            "Position: {}.\n"
                            "Words: '{}' and '{}'.\n"
                            "String numbers in dictionary: {} and {}."
                            "".format(
                                previous_word[index],
                                current_word[index],
                                index + 1,
                                previous_word,
                                current_word,
                                previous_position,
                                current_position
                            )
                        )
                    dg.add_edge(previous_word[index], current_word[index])
                    break
            else:
                if length_previous > length_current:
                    raise Exception(
                        "Wrong words order!\n"
                        "Words: '{}' and '{}'.\n"
                        "String numbers in dictionary: {} and {}."
                        "".format(
                            previous_word,
                            current_word,
                            previous_position,
                            current_position
                        )
                    )
            dg.add_nodes_from(current_word[index:])
            
            # move to the next word from dictionary
            previous_word = current_word
            previous_position = current_position
            current_word = dictionary.readline()
        
        # use topological sort to get the correct order of chars
        return topological_sort(dg)
    

if __name__ == '__main__':
    if not argv[1:]:
        print(restore_alphabet('alphabet.txt'))
    else:
        with open('result.txt', 'w') as alphabet:
            restoration_result = restore_alphabet(argv[1])
            for c in restoration_result[:-1]:
                alphabet.write(c + ", ")
            alphabet.write(restoration_result[-1])
