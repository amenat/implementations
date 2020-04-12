import os
import heapq
import pickle
from collections import Counter
from typing import Any, Dict, Tuple
from functools import total_ordering


@total_ordering
class Node:
    ''' The node object represents a Node in min-heap / huffman tree. '''

    def __init__(self, char: str, freq: int, is_internal=False, right=None, left=None) -> None:
        if not (isinstance(char, str) and len(char) == 1):
            raise ValueError('char of node should be of type str and length 1')
        if not isinstance(freq, int):
            raise ValueError('freq should be integer')
        if not isinstance(is_internal, bool):
            raise ValueError('in_internal should be boolean')
        if not all(map(lambda child: isinstance(child, Node) or child is None, [right, left])):
            raise ValueError('right and left should be Node or None.')

        self.char = char
        self.freq = freq
        self.is_internal = is_internal
        self.right = right
        self.left = left

    # dunder methods to ensure heapq works
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            raise ValueError(f'Can\'t compare Node to {type(other)}')
        return self.freq == other.freq

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Node):
            raise ValueError(f'Can\'t compare Node to {type(other)}')
        return self.freq < other.freq

    def __add__(self, other: object):
        ''' Sum of two nodes is defined as Node with freq equal to sum of operand freq.
            Resulting node points to operand nodes as right and left child
        '''
        if not isinstance(other, Node):
            raise ValueError(f'Can\'t add Node to {type(other)}')

        total_freq = self.freq + other.freq
        return Node('*', total_freq, is_internal=True, right=other, left=self)

    def __repr__(self):
        return f'({self.char} : {self.freq})'


def map_tree_to_dict(tree: Node, binary: str = '') -> Dict:
    '''Takes heap/tree and returns character -> binary string mapping'''
    mapping = dict()
    if not tree.is_internal:
        mapping[tree.char] = binary
    else:
        if tree.left:
            mapping.update(map_tree_to_dict(tree.left, binary + '0'))
        if tree.right:
            mapping.update(map_tree_to_dict(tree.right, binary + '1'))
    return mapping


# Adapted from: https://stackoverflow.com/questions/16887493/write-a-binary-integer-or-string-to-a-file-in-python
def bit_string_to_file(bitstring: str, filename: str) -> None:
    '''Takes bitstring as input and stores it in a file in binary form.'''
    bit_strings = [bitstring[i:i + 8] for i in range(0, len(bitstring), 8)]
    byte_list = [int(b, 2) for b in bit_strings]

    with open(filename, 'wb') as f:
        f.write(bytearray(byte_list))  # convert to bytearray before writing


def file_to_bitstring(filename: str) -> str:
    '''Reads compressed binary file and returns bitstring'''
    with open(filename, 'rb') as f:
        content = f.read()
    bitstring = ''
    for byte in content[:-1]:
        bitstring += f'{byte:08b}'

    # handle trailing byte seperately
    bitstring += f'{bin(content[-1])[2:]}'
    return bitstring


def huffman_encoding(data: str) -> Tuple[str, Node]:
    # convert data to dictionary with character frequency
    if not isinstance(data, str):
        raise ValueError('data should of type str')
    if len(data) == 0:
        raise ValueError('data must not be empty')

    char_freq = Counter(data)
    list_chars = [Node(char, freq, False) for char, freq in char_freq.items()]

    # convert to min-heap
    heapq.heapify(list_chars)

    # Special case of single string with same repeating character
    # a small optimization; since doing this for all cases means adding 1 extra unnecessary bit to all
    # characters and thus losing optimality of prefix codes.
    if len(list_chars) == 1:
        left_node = heapq.heappop(list_chars)
        right_node = Node('*', 0, False)       # dummy node
        new_internal_node = left_node + right_node
        heapq.heappush(list_chars, new_internal_node)
    else:
        while len(list_chars) >= 2:
            left_node = heapq.heappop(list_chars)
            right_node = heapq.heappop(list_chars)
            new_internal_node = left_node + right_node
            heapq.heappush(list_chars, new_internal_node)

    tree = list_chars[0]

    # treverse and and create mapping
    mapping = map_tree_to_dict(tree)

    # encode data
    char_data = list(data)

    compressed = ''
    for char in char_data:
        compressed += mapping[char]

    return compressed, tree

def huffman_decoding(data: str, tree: Node) -> str:
    ''' Decodes bitstring using huffman tree'''
    string = ''
    ptr = tree
    for i in range(len(data)):
        if data[i] == '0':
            ptr = ptr.left
        elif data[i] == '1':
            ptr = ptr.right
        if not ptr.is_internal:
            string += ptr.char
            ptr = tree
            continue

    return string


if __name__ == "__main__":

    print('-- Test: Alice in WonderLand full book --')

    book = 'alice.txt'
    with open(book, 'r', encoding='utf-8') as alice:
        data = alice.read()
    bitstring, tree = huffman_encoding(data)

    compressed_file = 'alice.dat'
    bit_string_to_file(bitstring, compressed_file)

    # Store tree in file
    treefile = 'alice.tree'

    with open(treefile, 'wb') as f:
        pickle.dump(tree, f)

    # create bitstring to decode
    to_decode = file_to_bitstring(compressed_file)

    # retrieve tree in file
    with open(treefile, 'rb') as f:
        tree = pickle.load(f)

    decoded = huffman_decoding(to_decode, tree)

    original_file_size = os.stat(book).st_size
    compressed_file_size = os.stat(
        compressed_file).st_size + os.stat(treefile).st_size

    print(f'Original file size: {original_file_size} bytes')
    print(f'Compressed file size: {compressed_file_size} bytes')
    print(f'Compression file is {100*(1 - compressed_file_size/original_file_size):.2f}% smaller')

    print(f'Does decoded data match orginal? : {data == decoded}')
