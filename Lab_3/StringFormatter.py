import re

class StringFormatter(object):
    
    def __init__(self):
        pass

    def delete_words(self, string, n):
        words = self.split_string(string)
        return ' '.join([word for word in words if len(word)>=n])

    def replace_numbers(self, string):
        return re.sub('\d', '*', string)

    def insert_spaces(self, string, separator = ' '):
        return separator.join(string)

    def sort_by_len(self, string):
        words = self.split_string(string)
        return ' '.join(sorted(words, key=len))

    def sort_by_lexgraph(self, string):
        words = self.split_string(string)
        return ' '.join(sorted(words, key=str.lower))
    
    def split_string(self, string):
        return string.replace('; ', ' ').replace(', ', ' ').replace('. ', ' ').replace(': ',' ').split(' ')