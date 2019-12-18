"""数据传输对象"""
import re


class Question(object):
    """封装数据库中的记录"""

    def __init__(self, id, description, answer, my_answer=None):
        self.id = id
        self.description = description
        self.answer = answer
        self.my_answer = my_answer
        self.format_description()

    def correct(self):
        return self.my_answer == self.answer

    def format_description(self):
        self.description = str(self.id) + '. ' + self.description
        self.description = re.sub(r'[\r\n\t]', '', self.description)
        self.description = re.sub(r'([A-D][\)、\.）])', r'\n\1', self.description)
