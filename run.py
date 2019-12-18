"""app.py"""
import cmd

from app.machines import ExamMachine


class CProgrammingExamShell(cmd.Cmd):
    """命令行应用程序"""

    intro = '欢迎使用C语言编程自测系统。输入 help 或 ? 查看命令。\n'
    prompt = '(shell) '

    def __init__(self, db_filename, **kwargs):
        super().__init__(**kwargs)
        self.exam_machine = ExamMachine(db_filename)

    def do_start(self, arg):
        try:
            qty = int(arg.split()[0])
        except Exception:
            print('参数非法！')
        else:
            self.exam_machine.start(qty)

    def do_answer(self, arg):
        try:
            ans = arg.split()[0]
        except Exception:
            print('参数非法！')
        else:
            self.exam_machine.answer(ans)

    def do_prev(self, arg):
        self.exam_machine.prev()

    def do_next(self, arg):
        self.exam_machine.next()

    def do_goto(self, arg):
        try:
            num = int(arg.split()[0])
        except Exception:
            print('参数非法！')
        else:
            self.exam_machine.goto(num)

    def do_submit(self, arg):
        self.exam_machine.submit()

    def do_history(self, arg):
        try:
            args = arg.split()
            history_id = int(args[0]) if len(args) > 0 else None
        except Exception:
            print('参数非法！')
        else:
            self.exam_machine.history(history_id)

    def do_quit(self, arg):
        """退出系统"""
        print('感谢您的使用！')
        self.exam_machine.conn.close()
        self.exam_machine.conn = None
        return True

    def precmd(self, line):
        """将所有命令转为小写"""
        return line.lower()


if __name__ == '__main__':
    CProgrammingExamShell('c_project.db').cmdloop()
