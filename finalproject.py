#Stephany YipChoy

import math
def clean_text(txt):
    """returns a list of the words in txt but cleaned"""
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace('-', '')
    txt = txt.replace('&', '')
    txt = txt.lower()

    clean = txt.split()

    return clean

def stem(s):
    """returns the stem of s"""
    if len(s) < 4:
        return s
    elif s[-2: ] == 'ly':
        return s[ :-2]
    elif s[-3 : ] == 'ing':
        return s[ : -3]
    elif s[-2 : ] == 'es':
        return s[ :-2]
    elif s[-1] == 'y':
        return s[ :-1] + 'i'
    elif s[-2: ] == 'er':
        if s[-3] == s[-4]:
            return s[ :-3]
        else:
            return s[ :-2]
    elif s[-1] == 'e':
        return s[ :-1]
    elif s[-1] == 's':
        return s[ :-1]
    else:
        return s

def compare_dictionaries(d1, d2):
    """computes and returns the log similarity score for the two dictionaries"""

    score = 0

    total = 0
    for word in d1:
        total += int(d1[word])

    for word in d2:
        if word in d1:
            score = score + math.log(int(d1[word]) / total) * int(d2[word])
        else:
            score = score + math.log(.5 / total) * int(d2[word])
    return score
    

class TextModel():
    """blueprint"""

    def __init__(self, model_name):
        """initializes the variables"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.syllable_counts = {}

    def __repr__(self):
        """returns a string w name of the model + dictionary sizes"""
        s = "text model name: " + str(self.name) + '\n'
        s += "  number of words: " + str(len(self.words)) + '\n'
        s += "  number of word lengths: " + str(len(self.word_lengths)) + '\n'
        s += "  number of stems: " + str(len(self.stems)) + '\n'
        s += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + '\n'
        s += "  number of syllable counts: " + str(len(self.syllable_counts))
        
        return s

    def add_string(self, s):
        """adds a strinf of text s to the model by augementing the featured dictionaries in the constructor"""

        word_list = s.split()
        last_end = -1
        for w in range(len(word_list)):

            if word_list[w][-1] in '.?!':
                sentence_len = len(word_list[last_end + 1: w]) + 1 
                last_end = w
                if sentence_len not in self.sentence_lengths:
                    self.sentence_lengths[sentence_len] = 1
                elif sentence_len in self.sentence_lengths:
                    self.sentence_lengths[sentence_len] += 1

        word_list = clean_text(s)

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            elif w in self.words:
                self.words[w] += 1

        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            elif len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1

        for w in word_list:
            w = stem(w)
            if w not in self.stems:
                self.stems[w] = 1
            elif w in self.stems:
                self.stems[w] += 1
                
        for w in word_list:
            vowels = 0
            for c in w:
                if c in 'aeiou':
                    vowels += 1
            if vowels not in self.syllable_counts:
                self.syllable_counts[vowels] = 1
            elif vowels in self.syllable_counts:
                self.syllable_counts[vowels] += 1

    def add_file(self, filename):
        """adds all of the text in the file to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        string = self.add_string(text)
        return string

    def save_model(self):
        """writes each dictionary to a file"""
        word_file = str(self.name) + '_words'
        length_file = str(self.name) + '_word_lengths'
        stems_file = str(self.name) + '_stems'
        sentence_lengths_file = str(self.name) + '_sentence_lengths'
        syllables_file = str(self.name) + 'syllable_counts'

        f = open(word_file, 'w')
        f.write(str(self.words))
        f.close

        ff = open(length_file, 'w')
        ff.write(str(self.word_lengths))
        ff.close

        fff = open(stems_file, 'w')
        fff.write(str(self.stems))
        fff.close

        ffff = open(sentence_lengths_file, 'w')
        ffff.write(str(self.sentence_lengths))
        ffff.close

        fffff = open(syllables_file, 'w')
        fffff.write(str(self.syllable_counts))
        fffff.close 

    def read_model(self):
        """reads stored dictionaries and assigns tem to attributes for TextModel"""
        word_file = str(self.name) + '_words'
        length_file = str(self.name) + '_word_lengths'
        stems_file = str(self.name) + '_stems'
        sentence_lengths_file = str(self.name) + '_sentence_lengths'
        syllables_file = str(self.name) + 'syllable_counts'

        f = open(word_file, 'r')
        word_str = f.read()
        f.close

        self.words = dict(eval(word_str))

        ff = open(length_file, 'r')
        length_str = ff.read()
        ff.close

        self.word_lengths = dict(eval(length_str))

        fff = open(stems_file, 'r')
        stems_str = fff.read()
        fff.close

        self.stems = dict(eval(stems_str))

        ffff = open(sentence_lengths_file, 'r')
        sentence_lengths_str = ffff.read()
        ffff.close

        self.sentence_lengths = dict(eval(sentence_lengths_str))

        fffff = open(syllables_file, 'r')
        syllables_str = fffff.read()
        fffff.close

        self.syllable_counts = dict(eval(syllables_str))

    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores meansuring the similarity of self and other"""
        scores = []

        word_score = compare_dictionaries(other.words, self.words)
        scores += [word_score]

        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        scores += [word_length_score]

        stem_score = compare_dictionaries(other.stems, self.stems)
        scores += [stem_score]

        sentence_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        scores += [sentence_score]

        syllable_score = compare_dictionaries(other.syllable_counts, self.syllable_counts)
        scores += [syllable_score]

        return scores

    def classify(self, source1, source2):
        """compares self to two other textmodel objects and determines which of them is most likely the source of self"""

        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print('scores for', source1.name, ': ', scores1)
        print('scores for', source2.name, ': ', scores2)

        weighted_sum1 = scores1[0] + .7*scores1[1] + .5*scores1[2] + scores1[3] + .7*scores1[4]
        weighted_sum2 = scores2[0] + .7*scores2[1] + .5*scores2[2] + scores2[3] + .7*scores2[4]

        if weighted_sum1 > weighted_sum2:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)
def test():
    """ test code """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ compares my samples to last week tn scripts and NYT articles"""
    source1 = TextModel('last week tonight')
    source1.add_file('lastweektonight.txt')

    source2 = TextModel('new york times')
    source2.add_file('newyorktimes.txt')

    new1 = TextModel('wr151')
    new1.add_file('wr151.txt')
    new1.classify(source1, source2)

    new2 = TextModel('tomi_lahren')
    new2.add_file('tomilahren.txt')
    new2.classify(source1, source2)

    new3 = TextModel('trump')
    new3.add_file('trump.txt')
    new3.classify(source1, source2)

    new4 = TextModel('obama_tweet')
    new4.add_file('obama tweet.txt')
    new4.classify(source1, source2)

    

    

