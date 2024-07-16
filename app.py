from flask import Flask, render_template, redirect, session, request, flash
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session['responses'] = []
        return redirect('/questions/0')
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def question(qid):
    responses = session.get('responses', [])
    if qid != len(responses):
        flash("Invalid question access.")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid, survey=satisfaction_survey)

@app.route('/answer', methods=["POST"])
def answer():
    answer = request.form['answer']
    responses = session.get('responses', [])
    responses.append(answer)
    session['responses'] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html', survey=satisfaction_survey)

if __name__ == "__main__":
    app.run(debug=True)
