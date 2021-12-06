# text correction
- it's a scalable auto text correction built with some sense of OOP 

- currently support a naive spelling of simple argmax function over the most likely transformation of each word within your choice of edits number and result number as well.

- works with any language

- data can be json file, text file and even raw data.

- note that the auto-correction isn't perfect, the algorithm has no sense of the semantics.

your only three steps away from consuming this package see the example to get the result below.
# execution example
``` shell
naive@bayes:~/textcorrection$ python3 example.py
total number of alphabet is: 26
total number of loaded words is: 69944
total number of unique words is: 69944
type something ..:
headacha
suggestion number 1 is: headache
suggestion number 2 is: headacha
```

# dataset
Note: All data files should be under Data folder
- Egyptian arabic vocabulary set can be found here [Egyptian Arabic wikipedia](https://drive.google.com/file/d/1bgDu-LFQRB0wHGtRCCqJW5Gg_4DDDB0G/view?usp=sharing)
- Medical terms and vocabulary set can be found here[Medical Vocab](https://github.com/socd06/medical-nlp/blob/master/data/vocab.txt)

