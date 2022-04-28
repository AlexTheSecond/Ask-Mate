import datetime
from flask import Flask, render_template, request, redirect
import data_handler
import additional_functions
import templates
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024

@app.route("/")
@app.route('/list')
def route_list():
    questions = data_handler.get_questions()
    order_direction = request.args.get("order_direction", "desc")
    order_by = request.args.get("order_by", "title")
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == 'desc'))
    return render_template('list.html', user_question=questions)


@app.route('/question/<q_id>')
def view_question(q_id):
    select_question = data_handler.get_question(q_id)
    select_answer = data_handler.get_answer(q_id)
    return render_template('question.html', selected_question=select_question, selected_answer=select_answer)


@app.route('/add-question', methods=['POST', 'GET'])
def add_new_question():
    if request.method == "GET":
        return render_template('newquestion.html')
    data_handler.add_question()
    new_question_index = data_handler.get_last_id()
    return redirect(f"/question/{str(new_question_index[0]['max'])}")


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('newanswer.html', question_id=question_id)
    data_handler.add_answer(question_id)
    return redirect(f"/question/{str(question_id)}")


@app.route('/question/<q_id>/delete')
def delete_question(q_id):
    data_handler.delete_question(q_id)
    return redirect("/list")


@app.route('/question/<q_id>/edit', methods=['POST', 'GET'])
def edit_question(q_id):
    if request.method == 'GET':
        select_question = data_handler.get_all_question(q_id)
        return render_template('editquestion.html', selected_question=select_question)

    questions = data_handler.get_all_question()
    for item in questions:
        if item['id'] == str(q_id):
            item['title'] = request.form['title'] if 'title' in request.form else item['title']
            item['message'] = request.form['message'] if 'message' in request.form else item['message']
    data_handler.write_table_to_file_question(data_handler.create_list_to_write(questions))
    return redirect(f"/question/{str(q_id)}")


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    q_id = data_handler.get_id(int(answer_id))
    data_handler.delete_answer(answer_id)
    return redirect(f"/question/{str(q_id[0]['question_id'])}")


@app.route('/question/<question_id>/<vote>')
def vote_question(question_id, vote):
    questions = data_handler.get_all_question()
    questions = additional_functions.vote(questions, question_id, 1 if vote == 'vote-up' else -1)
    # if vote == 'vote-up':
    #     for item in questions:
    #         if item['id'] == question_id:
    #             item['vote_number'] = str(int(item['vote_number']) + 1)
    # elif vote == 'vote-down':
    #     for item in questions:
    #         if item['id'] == question_id:
    #             item['vote_number'] = str(int(item['vote_number']) + 1)
    data_handler.write_table_to_file_question(data_handler.create_list_to_write(questions))
    return redirect("/list")


@app.route('/answer/<answer_id>/<vote>')
def vote_answer(answer_id, vote):
    answers = data_handler.get_all_answer()
    question_id = int([a['question_id'] for a in answers if a['id'] == answer_id].pop())
    answers = additional_functions.vote(answers, answer_id, 1 if vote == 'vote-up' else -1)
    data_handler.write_table_to_file_answer(data_handler.create_list_to_write(answers))
    return redirect(f"/question/{str(question_id)}")


if __name__ == "__main__":
    app.run()
