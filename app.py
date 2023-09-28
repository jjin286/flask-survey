from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def home():
    """Returns the start survey page"""

    session["responses"] = []

    return render_template(
        "survey_start.html",
        survey=survey)


@app.post("/begin")
def begin():
    """Redirects to start survey"""

    return redirect("/questions/0")


@app.get("/questions/<int:question_num>")
def show_question(question_num):
    """Returns question number question_num"""

    num_of_responses = len(session["responses"])

    if num_of_responses == question_num:
        return render_template(
            "question.html",
            question=survey.questions[question_num])

    elif num_of_responses == len(survey.questions):
        flash("You've already completed the survey!")
        return redirect("/completion")

    else:
        flash(f"You haven't answered question { num_of_responses }")
        return redirect(f"/questions/{ num_of_responses }")



@app.post("/answer")
def handle_answer():
    """Store answer locally and redirect to next question"""

    answer = request.form.get('answer')
    curr_question_index = len(session['responses'])
    survey_question_count = len(survey.questions)

    if(answer):
        responses = session['responses']
        responses.append(answer)
        session['responses'] = responses

        curr_question_index = len(session['responses'])

        if(curr_question_index == survey_question_count):
            return redirect("/completion")

        return redirect(f"/questions/{curr_question_index}")

    else:
        flash("Please select a choice before continuing")

        return redirect(f"/questions/{curr_question_index}")


@app.get("/completion")
def complete():
    """Return completed survey page"""

    survey_question_count = len(session['responses'])

    return render_template(
                "completion.html",
                question_count=survey_question_count,
                questions=survey.questions)

