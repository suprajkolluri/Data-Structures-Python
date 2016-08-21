__author__ = 'Supraj'

import sys
INFINITY = sys.maxint

'''
Takes in a test file of multiple words as inputs and
uses a dynamic programming approach to format the output to
contain optimum number of words per line
'''


def print_neatly(words, M):
    """ Print text neatly.
    Parameters
    ----------
    words: list of str
        Each string in the list is a word from the file.
    M: int
        The max number of characters per line including spaces

    Returns
    -------
    cost: number
        The optimal value as described in the textbook.
    text: str
        The entire text as one string with newline characters.
        It should not end with a blank line.

    Details
    -------
        Look at print_neatly_test for some code to test the solution.

    >>> words = ['In', 'Xanadu', 'did', 'KubIa', 'Khan', 'A', 'stately', 'pleasure', 'dome', 'decree:', 'Where', 'Alph,', 'the', 'sacred', 'river,']
    >>> M = 80
    >>> print_neatly(words, M)
    (512, 'In Xanadu did KubIa Khan A stately pleasure dome decree: Where Alph, the\\nsacred river,')
    """

    word_count = len(words)
    text = ''
    (prev_list, cost) = create_lists(words, M)

    temp = word_count
    while True:
        curr_val = prev_list[temp - 1]
        curr_line = words[curr_val]
        for i in range(curr_val + 1, temp):
            curr_line += ' ' + words[i]
        if temp != word_count:
            text = curr_line + '\n' + text
        else:
            text = curr_line

        temp = curr_val

        if(temp == 0):
            break

    return cost, text

'''
Computing the line cost based on the number of
extra spaces calculated when words from index
i to j are arranged in a single line
'''


def query_line_cost(space_left, word_count, ind):

    cost = 0
    if(space_left < 0):
        cost = INFINITY
    elif(space_left >= 0 and ind == word_count - 1):
        cost = 0
    else:
        cost = space_left ** 3

    return cost


def create_lists(words, M):

    # Represents the total number of words in the input text file
    word_count = len(words)

    # Indicates the number of extra spaces when words from index i to j are arranged in one line
    extra_space = [[0 for m in range(word_count)] for m in range(word_count)]

    # Indicates the cost of a line that has words from word index i to j
    line_cost_list = [[0 for m in range(word_count)] for m in range(word_count)]

    # Indicates the optimal cost for arranging words from 1 to i
    cost_list = [0 for m in range(word_count)]

    # Used in printing the final solution
    prev_list = [0 for m in range(word_count)]

    # Looping to calculate the number of extra spaces needed when words from index i to j are arranged in a single line
    for i in range(0, word_count):
        extra_space[i][i] = M - len(words[i])
        line_cost_list[i][i] = query_line_cost(extra_space[i][i], word_count, i)
        for j in range(i + 1, word_count):
            extra_space[i][j] = extra_space[i][j - 1] - len(words[j]) - 1
            line_cost_list[i][j] = query_line_cost(extra_space[i][j], word_count, j)

    # Looping to find the minimum cost arrangement. cost_list indicates the minimum cost to print words from word index 1 to i
    for i in range(0, word_count):
        cost_list[i] = INFINITY
        for j in range(0, i):
            if cost_list[j - 1] + line_cost_list[j][i] < cost_list[i]:
                cost_list[i] = cost_list[j - 1] + line_cost_list[j][i]
                prev_list[i] = j

    return prev_list, cost_list[-1]
