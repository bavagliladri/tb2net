import random
import pandas as pd


class Token:
    def __init__(self, id, form, lemma, upos, head, deprel):
        # defines a token in a UD treebank
        self.id = id
        self.form = form
        self.head = head
        self.lemma = lemma
        self.upos = upos
        self.deprel = deprel


class Sentence:
    def __init__(self):
        # defines a sentence as a collection of tokens
        self.tokens = []

    def add_token(self, token):
        # adds a token to a sentence
        if type(token) is Token:
            self.tokens.append(token)
        else:
            raise ValueError(f'Could not add {token} to the sentence')

    def get_head(self, token):
        # takes a token as argument and return the head of the syntactic relation (if present)
        # if the token is the root of the sentence returns False
        # if the token points towards a position that is not in the sentence raises an error
        head_position = token.head
        if head_position == 0:
            return False
        found_head = False
        for head in self.tokens:
            if head.id == head_position:
                found_head = True
                break
        if found_head:
            return head
        else:
            raise ValueError(f'The head of {token.form} is not in the sentence')

    def get_size(self):
        # returns the number of tokens in the sentence
        return len(self.tokens)


class Treebank:
    def __init__(self):
        # defines a treebank as a collection of sentences
        self.sentences = []

    def add_sentence(self, sentence):
        # adds a sentence to a treebank
        if type(sentence) is Sentence:
            self.sentences.append(sentence)
        else:
            raise ValueError(f'Could not add {sentence} to the treebank')

    def get_size(self):
        # returns the number of tokens in the treebank
        size = 0
        for sent in self.sentences:
            size += sent.get_size()
        return size

    def reduce2size(self, size):
        # selects randomly some sentences until the desired size is reached
        random.seed(size)
        ids_sent = list(range(len(self.sentences)))
        random.shuffle(ids_sent)
        new = self.sentences.copy()
        self.sentences = []
        for x in ids_sent:
            if self.get_size() > size:
                break
            self.add_sentence(new[x])

    def get_node_list(self, word_based = True):
        # returns the list of the tokens in the treebank
        nodes = set()
        for sent in self.sentences:
            for tok in sent.tokens:
                if word_based:
                    nodes.add((tok.form, tok.upos))
                else:
                    nodes.add((tok.lemma, tok.upos))
        return nodes

    def get_edge_list(self, word_based = True):
        # returns the list of the syntactic links in the treebank
        # each syntactic link is unique in the list and consists of two elements:
        # the former is the head of the syntactic link, the latter is the dependent
        edges = set()
        for sent in self.sentences:
            for tok in sent.tokens:
                head = sent.get_head(tok)
                if head:
                    if word_based:
                        e = ((head.form, head.upos), (tok.form, tok.upos), tok.deprel)
                    else:
                        e = ((head.lemma, head.upos), (tok.lemma, tok.upos), tok.deprel)
                    edges.add(e)
        return edges

    def net_files(self, word_based = True, output_nodes = 'nodes.csv', output_edges = 'edges.csv'):
        # this functions produces two files:
        # - nodes_file: csv file with three columns (id, form/lemma, upos)
        # - edges_file: csv file with three columns (parent_id, child_id, deprel)
        # parent_id and child_id refer to the element stored in the nodes_file
        nodes = self.get_node_list(word_based)
        edges = self.get_edge_list(word_based)

        n_dict = {}
        id = 0
        for n in nodes:
            n_dict[n] = id
            id += 1

        e_list = set()
        for e in edges:
            id_parent = n_dict[e[0]]
            id_child = n_dict[e[1]]
            e_list.add((id_parent, id_child, e[2]))

        if word_based:
            col_name = 'form'
        else:
            col_name = 'lemma'
        nodes_df = pd.DataFrame({'id': list(n_dict.values()),
                                 col_name: [x[0] for x in n_dict.keys()],
                                 'pos': [x[1] for x in n_dict.keys()]},
                                columns=['id', col_name, 'pos'])
        edges_df = pd.DataFrame({'parent_id': [x[0] for x in e_list],
                                 'child_id': [x[1] for x in e_list],
                                 'deprel': [x[2] for x in e_list]},
                                columns=['parent_id', 'child_id', 'deprel'])

        nodes_df.to_csv(output_nodes, index=False)
        edges_df.to_csv(output_edges, index=False)


def build_tb(ud_file):
    # this function takes as argument a UD file and returns a Treebank object
    with open(ud_file, 'r') as file:
        lines = file.readlines()

    sentence = Sentence()
    treebank = Treebank()
    for l in lines:
        if l[0] not in '#\n':
            fields = l.split('\t')
            if '.-' not in fields[0]:
                id, form, lemma, upos, head, deprel = int(fields[0]), fields[1], fields[2], fields[3], int(fields[6]), fields[7]
                token = Token(id, form, lemma, upos, head, deprel)
                if token.upos not in ['PUNCT', 'SYM']:
                    sentence.add_token(token)
        else:
            if sentence.get_size() != 0:
                treebank.add_sentence(sentence)
                sentence = Sentence()
    return treebank


if __name__ == '__main__':
    tb = build_tb('test.conllu')
    string = ''
    for tok in tb.sentences[0].tokens:
        string += tok.form + ' '
    print(f'The first sentence of the treebank is:\n{string}')
