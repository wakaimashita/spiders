import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords

brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
     ])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"

class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    def extract(self,stop_list):
        tokens = self.tokenize_sentence(self.sentence)

        stop_words = set(stop_list+stopwords.words('english'))

        # filtered_sentence = [w for w in tokens if not w in stop_words]
        # print(filtered_sentence)

        filtered_sentence = tokens
        # filtered_sentence = []
        #
        # for w in tokens:
        #     if w not in stop_words:
        #         filtered_sentence.append(w)
        # print(filtered_sentence)

        tags = self.normalize_tags(bigram_tagger.tag(filtered_sentence))
        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break
        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
                matches.append(t[0])
        return matches


def main():

    item_list = []
    stop_list = []
    with open('englishWord.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())

    with open('stopWords.txt') as f:
        results = f.readlines()
        for res in results:
            stop_list.append(res.strip())

    for sentence in item_list:
        print(sentence)
        np_extractor = NPExtractor(sentence)
        result = np_extractor.extract(stop_list)
        # print(result)
        endResult = []
        for res in result:
            if len(res.split(' ')) == 1:
                continue
            res = res.replace('﻿','')
            endResult.append(res)
        print(endResult)
        with open('结果.txt','a') as f:
            f.write(sentence+'\n'+str(endResult)+'\n')



if __name__ == '__main__':
    main()