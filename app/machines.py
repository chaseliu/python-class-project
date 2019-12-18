"""状态机"""
import os
import sqlite3

from .states import InExamState, OutExamState
from .db import query_questions, query_history, query_history_detail


class ExamMachine(object):

    def __init__(self, db_filename):
        self.in_exam_state = InExamState(self)
        self.out_exam_state = OutExamState(self)
        self.state = self.out_exam_state
        self.history_id = None
        self.questions = []
        self.conn = sqlite3.connect(db_filename)
        self.idx = 0

    def start(self, qty):
        self.state.start(qty)

    def submit(self):
        self.state.submit()

    def goto(self, num):
        self.state.goto(num)

    def prev(self):
        self.state.prev()

    def next(self):
        self.state.next()

    def answer(self, ans):
        self.state.answer(ans)

    def history(self, history_id=None):
        self.state.history(history_id)

    def print_current(self):
        """打印当前题目"""
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('第{}道题：'.format(self.idx + 1))
        current = self.questions[self.idx]
        print(current.description)
        print('我的答案：{}'.format(current.my_answer if current.my_answer else '未填写'))

    def print_history(self):
        """打印答题记录"""
        for history in query_history(self.conn):
            print('id={}\t开始时间={}\t结束时间={}\t得分={}'.format(
                history[0],
                history[1][:16],
                history[2][:16],
                history[3],
            ))

    def load_questions(self, limit=10):
        """从题库中加载题目"""
        self.questions = list(query_questions(self.conn, limit))
        self.idx = 0
        self.history_id = create_history(self.conn)
        self.print_current()

    def load_answers(self, history_id):
        self.history_id = history_id
        self.questions = list(query_history_detail(self.conn, self.history_id))

    def save_answers(self):
        """保存本次答题的答案"""
        save_answers(self.conn, self.history_id, self.calc_socre(), self.questions)

    def calc_socre(self):
        """计算并打印成绩"""
        right = 0
        for i, q in enumerate(self.questions):
            print('=' * 20)
            print('第{}题'.format(i + 1))
            print('-' * 20)
            print(q.description)
            print('-'*20)
            if q.correct():
                print('您的选项为{}, 恭喜您答对了！'.format(q.my_answer))
                right += 1
            else:
                print('您的选项为{}，正确选项为{}，您回答错了！'.format(q.my_answer, q.answer))
        print('=' * 40)
        score = right * 100 / len(self.questions)
        print('您的正确率为：%.2f%%' % score)
        return score
