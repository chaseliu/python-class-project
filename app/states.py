"""状态机状态"""

class State(object):
    """状态接口"""

    def start(self, qty):
        raise NotImplementedError

    def submit(self):
        raise NotImplementedError

    def goto(self, num):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def answer(self, ans):
        raise NotImplementedError

    def history(self, history_id):
        raise NotImplementedError


class InExamState(State):
    """答题中状态，此时只能上一题/下一题/答题，全部打完后才能提交"""

    def __init__(self, exam_machine):
        self.exam_machine = exam_machine

    def history(self, history_id):
        print('请继续答题！')

    def start(self, qty):
        print('请继续答题！')

    def submit(self):
        if all(map(lambda x: x.my_answer, self.exam_machine.questions)):
            self.exam_machine.save_answers()
            self.exam_machine.state = self.exam_machine.out_exam_state
        else:
            nums = ', '.join(str(i+1) for i, q in enumerate(self.questions) if not q.my_answer)
            print('第{}题还未回答！请使用goto命令跳转至该题作答'.format(nums))

    def answer(self, ans):
        if ans in ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd']:
            self.exam_machine.questions[self.exam_machine.idx].my_answer = ans.upper()
            # 回答完成后自动跳入下一题
            self.next()
        else:
            print('输入有误，请重新输入！')

    def goto(self, num):
        idx = num - 1
        questions_len = len(self.exam_machine.questions)
        if not 0 <= idx < questions_len:
            print('请输入1～{}数值！'.format(questions_len))
        else:
            self.exam_machine.idx = idx
            self.exam_machine.print_current()

    def prev(self):
        """上一题"""
        if self.exam_machine.idx <= 0:
            print('已经是第一道题')
        else:
            self.exam_machine.idx -= 1
            self.exam_machine.print_current()

    def next(self):
        """下一题"""
        questions_len = len(self.exam_machine.questions)
        if self.exam_machine.idx >= questions_len - 1:
            print('已经是最后一道题')
        else:
            self.exam_machine.idx += 1
            self.exam_machine.print_current()


class OutExamState(State):
    """本次答题未开始/已完成，可以查看本次得分、查看历史得分、开启新的答题"""

    def __init__(self, exam_machine):
        self.exam_machine = exam_machine

    def start(self, qty):
        self.exam_machine.load_questions(qty)
        print('{}道题目加载完毕！输入answer答题；输入prev/next查看前后题'.format(qty))
        self.exam_machine.state = self.exam_machine.in_exam_state
        self.exam_machine.print_current()

    def submit(self):
        print('请先开始答题！')

    def goto(self, num):
        print('请先开始答题！')

    def prev(self):
        print('请先开始答题！')

    def next(self):
        print('请先开始答题！')

    def answer(self, ans):
        print('请先开始答题！')

    def history(self, history_id):
        if history_id:
            self.exam_machine.load_answers(history_id)
            if self.exam_machine.questions:
                self.exam_machine.calc_socre()
            else:
                print('无答题记录！')
        else:
            self.exam_machine.print_history()
