import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP
NP -> N | P NP | NP NP | Det NP | NP Adv | AP NP
VP -> V | VP NP | Adv VP | VP Adv
AP -> Adj | Adj AP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #convert sentence to list of words with tokenize
    words = nltk.tokenize.wordpunct_tokenize(sentence.lower())

    #exclude words without at least one alphabetic character
    for word in words:
        contains_alphabetic = False

        #loop through letters and see if one is alpha.
        for letter in word:
            if letter.isalpha():
                contains_alphabetic = True

        #remove word if no alphabetic
        if contains_alphabetic == False:
            words.remove(word)

    #return words.
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = list()
    checked_subtrees = list()

    #loop through tree
    for i in range(tree.height()):
        for subtree in tree.subtrees(lambda tree: tree.height() == i):

            #check if subtree is NP
            if subtree.label() == "NP":

                #check if new NP already has an intersection with already checked NPs. if not -> add tree
                if not (set(checked_subtrees).intersection(set(subtree.leaves()))):
                    chunks.append(subtree)
                checked_subtrees = checked_subtrees + subtree.leaves()

    return chunks


if __name__ == "__main__":
    main()
