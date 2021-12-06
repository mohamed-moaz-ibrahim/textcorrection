import json

ALPHABET = ''
__WORDS_POOL = []
_WORD_PROBABILITY_DICTIONARY = {}

class WORDSPOOL(object):
    def __init__(self, verbose = False):
        self.verbose = verbose

    def create_words_pool_from_json(self, path, alphabet):
        global __WORDS_POOL, ALPHABET
        ALPHABET = alphabet
        with open(path) as file:
            words_pool = []
            for line in file:
                essay = json.loads(line)['text']
                words_pool += [word for word in essay.split()]
            __WORDS_POOL = words_pool
        self.__calc_word_probability()

    def create_words_pool_from_text_file(self, path, alphabet):
        global __WORDS_POOL, ALPHABET
        ALPHABET = alphabet
        with open(path) as file:
            words_pool = []
            for line in file:
                words_pool += [word for word in line.split()]
            __WORDS_POOL = words_pool
        self.__calc_word_probability()

    def create_words_pool_from_text(self, text, alphabet):
        global __WORDS_POOL, ALPHABET
        __WORDS_POOL = text.split()
        ALPHABET = alphabet
        self.__calc_word_probability()

    def __count_pool(self):
        global _WORD_PROBABILITY_DICTIONARY
        for word in __WORDS_POOL:
            _WORD_PROBABILITY_DICTIONARY[word] = _WORD_PROBABILITY_DICTIONARY.get(word,0) + 1

    def __calc_word_probability(self):
        global _WORD_PROBABILITY_DICTIONARY
        self.__count_pool()
        for word, repetition in _WORD_PROBABILITY_DICTIONARY.items():
            probability = repetition / len(__WORDS_POOL)
            _WORD_PROBABILITY_DICTIONARY[word] = (repetition, probability)
            if self.verbose: print(f'word: {word}, repetition: {repetition}, probability: {probability}')
        print(f'total number of alphabet is: {len(ALPHABET)}')
        print(f'total number of loaded words is: {len(__WORDS_POOL)}')
        print(f'total number of unique words is: {len(_WORD_PROBABILITY_DICTIONARY)}')

class WORDTRANSFORMATION(object):
    def __init__(self, char_deleting = True, char_swaping = True, char_inserting = True, char_replacing = True, verbose = False):
        self.char_deleting = char_deleting
        self.char_swaping = char_swaping
        self.char_inserting = char_inserting
        self.char_replacing = char_replacing
        self.verbose = verbose
    
    def transform(self, word_list_of_tuple):
        transformed_word_list = []
        current_length = len(transformed_word_list)
        if self.verbose: print(f'word list in process: {word_list_of_tuple}')
        for word, probability in word_list_of_tuple:
            if self.char_deleting:
                for i in range(len(word)):
                    transformed_word = word[:i]+ word[i:][1:]
                    probability = _WORD_PROBABILITY_DICTIONARY.get(transformed_word,(0,0))[1]
                    transformed_word_list.append( ( transformed_word, probability ) )  
                if self.verbose: print(f'word list after deleting: {transformed_word_list[current_length:]}')
                current_length = len(transformed_word_list)
            if self.char_swaping:
                for i in range(len(word)):
                    if len(word[i:])>=2:
                        transformed_word = word[:i]+word[i+1]+word[i]+word[i+2:]
                        probability = _WORD_PROBABILITY_DICTIONARY.get(transformed_word,(0,0))[1]
                        transformed_word_list.append((transformed_word, probability) )
                if self.verbose: print(f'word list after swapping: {transformed_word_list[current_length:]}')
                current_length = len(transformed_word_list)
            if self.char_inserting:
                for i in range(len(word) + 1):
                    for c in ALPHABET:
                        transformed_word  = word[:i]+c+word[i:]
                        probability = _WORD_PROBABILITY_DICTIONARY.get(transformed_word,(0,0))[1]
                        transformed_word_list.append( (transformed_word, probability) )
                if self.verbose: print(f'word list after inserting: {transformed_word_list[current_length:]}')
                current_length = len(transformed_word_list)
            if self.char_replacing:
                for i in range(len(word)):
                    for c in ALPHABET:
                        if len(word)-i>=1 and word[i]!=c:
                            transformed_word  = word[:i]+c+word[i+1:]
                            probability = _WORD_PROBABILITY_DICTIONARY.get(transformed_word,(0,0))[1]
                            transformed_word_list.append( (transformed_word, probability) )
                if self.verbose: print(f'word list after replacing: {transformed_word_list[current_length:]}')
                current_length = len(transformed_word_list)
        return transformed_word_list

class SPELLING(WORDSPOOL):
    def __init__(self, number_of_suggestion_result = 1, number_of_letters_to_transform = 2, char_deleting = True, char_swaping = True, char_inserting = True, char_replacing = True, verbose = False):
        super().__init__(verbose)
        self.number_of_suggestion_result = number_of_suggestion_result
        self.number_of_letters_to_transform = number_of_letters_to_transform
        self.char_deleting = char_deleting
        self.char_swaping = char_swaping
        self.char_inserting = char_inserting
        self.char_replacing = char_replacing
        self.verbose = verbose

    def __get_suggestions(self,word):
        word_transformation = WORDTRANSFORMATION(char_deleting = self.char_deleting,
         char_swaping = self.char_swaping, char_inserting = self.char_inserting,
          char_replacing = self.char_replacing,verbose= self.verbose)

        suggestion_list = word_transformation.transform([(word, 0)])
        for i in range(1, self.number_of_letters_to_transform):
            suggestion_list += word_transformation.transform(suggestion_list)
        return sorted(suggestion_list, key= lambda suggested_tuple:suggested_tuple[1], reverse=True)

    def get_most_frequent(self,text):
        text_best_match = ['' for i in range(self.number_of_suggestion_result)]
        for word in text.split():
            if _WORD_PROBABILITY_DICTIONARY.get(word) == None:
                word_suggestion_list_of_tuples = self.__get_suggestions(word)
                if self.verbose: print(f"suggested list: {word_suggestion_list_of_tuples}")
                if self.verbose: print(f"total suggested words: {len(word_suggestion_list_of_tuples)}")
             
            # naive way to correct each word it will mostly correct only spelling but wrong context
            #print the same word if not found or the probability after transforming is also zero
            for i in range(self.number_of_suggestion_result):
                text_best_match[i] += word_suggestion_list_of_tuples[i][0] \
                          if _WORD_PROBABILITY_DICTIONARY.get(word) == None and \
                              word_suggestion_list_of_tuples[i][1] > 0 else word + ' '
        
        return text_best_match