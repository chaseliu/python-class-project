"""数据库操作"""
import datetime

from .dtos import Question


def query_questions(conn, limit=10):
    """sqlite数据库查询操作"""
    sql = 'SELECT ID, description, answer FROM question_bank ORDER BY RANDOM()'
    if limit and isinstance(limit, int):
        sql += ' LIMIT {}'.format(limit)
    sql += ';'
    cursor = conn.cursor()
    for record in cursor.execute(sql):
        yield Question(*record)
    cursor.close()


def create_history(conn):
    """创建答题历史记录"""
    now_str = datetime.datetime.now().isoformat()
    sql = 'INSERT INTO history(start_time) VALUES (?);'
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (now_str,))
        cursor.close()
    return cursor.lastrowid


def save_answers(conn, history_id, score, questions):
    """保存答题记录中的答案"""
    now_str = datetime.datetime.now().isoformat()
    with conn:
        cursor = conn.cursor()
        sql = 'UPDATE history SET end_time = ?, score = ? WHERE id = ?;'
        cursor.execute(sql, (now_str, score, history_id))
        sql = 'DELETE FROM answers WHERE history_id = ?;'
        cursor.execute(sql, (history_id,))
        sql = 'INSERT INTO answers(history_id, question_id, answer) VALUES (?, ?, ?);'
        cursor.executemany(sql, ((history_id, x.id, x.my_answer,) for x in questions))
        cursor.close()


def query_history(conn):
    sql = 'SELECT id, start_time, end_time, score FROM history;'
    cursor = conn.cursor()
    for record in cursor.execute(sql):
        yield record
    cursor.close()


def query_history_detail(conn, history_id):
    sql = '''
        SELECT t1.question_id, t2.description, t2.answer, t1.answer AS my_answer
        FROM answers AS t1
        INNER JOIN question_bank AS t2 ON t1.question_id = t2.id
        WHERE t1.history_id = ?;
    '''
    cursor = conn.cursor()
    for record in cursor.execute(sql, (history_id,)):
        yield Question(*record)
    cursor.close()
