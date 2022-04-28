import os
import datetime
DATA_FILE_PATH_QUESTION = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWER = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']
from flask import request
import additional_functions

import database_common


@database_common.connection_handler
def get_questions(cursor):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, q_id):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            WHERE id = %s
            ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_answer(cursor, q_id):
    query = """
           SELECT id, submission_time, vote_number, question_id, message, image
           FROM answer
           WHERE question_id = %s
           ORDER BY submission_time"""
    cursor.execute(query, (q_id,))
    return cursor.fetchall()




@database_common.connection_handler
def get_answers(cursor):
    query = """
           SELECT id, submission_time, vote_number, question_id, message, image
           FROM answer
           ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def add_question(cursor):
    #new_submission = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
    new_title = request.form.get('title', default="")  # poprawic
    new_message = request.form['message']
    upload_file = request.files['file']
    new_image = additional_functions.file_operation(upload_file)
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES (now(), 0, 0, %s, %s, %s);    
    """
    cursor.execute(query, (new_title, new_message, new_image))

@database_common.connection_handler
def get_last_id(cursor):
    query = """
            SELECT max(id) FROM question"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def add_answer(cursor,question_id):
    new_message = request.form['message']
    upload_file = request.files['file_answer']
    new_image = additional_functions.file_operation(upload_file)
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
        VALUES (now(), 0, %s, %s, %s);    
    """
    cursor.execute(query, (question_id, new_message, new_image))


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id= %s;
    """
    cursor.execute(query, (question_id,))

@database_common.connection_handler
def update_question(cursor, question_id):
    new_title = request.form.get('title', default="")
    new_message = request.form['message']
    query = """
        UPDATE question 
        SET title= %s, message =%s
     WHERE id = %s;
    """
    cursor.execute(query, (new_title,new_message,int(question_id)))



def create_list_to_write(list):
    list_to_return=[]
    for item in list:
        list_to_return.append(item.values())
    return list_to_return


def write_table_to_file_question(table, separator=','):
    with open(DATA_FILE_PATH_QUESTION, "w") as file:
        for record in table:
            row = separator.join(record)
            file.write(row + "\n")
@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
           DELETE
           FROM answer
           WHERE id = %s"""
    query_1 = """
            DELETE
            FROM comment
            WHERE answer_id = %s"""

    cursor.execute(query_1, (answer_id,))
    cursor.execute(query, (answer_id,))

def write_table_to_file_answer(table, separator=','):
    with open(DATA_FILE_PATH_ANSWER, "w") as file:
        for record in table:
            row = separator.join(record)
            file.write(row + "\n")

@database_common.connection_handler
def get_id(cursor, answer_id):
    query = """
           SELECT question_id
           FROM answer
           WHERE id = %s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()
