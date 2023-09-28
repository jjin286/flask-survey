from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def home():
    """Returns the start survey page"""

    return render_template(
        "survey_start.html",
        survey=survey)


@app.post("/begin")
def begin():
    """Redirects to start survey"""

    responses.clear() #Clear everytime we start a new survey

    return redirect("/questions/0")


@app.get("/questions/<int:question_num>")
def show_question(question_num):
    """Returns question number question_num"""

    return render_template(
        "question.html",
        question=survey.questions[question_num])


@app.post("/answer")
def handle_answer():
    """Store answer locally and redirect to next question"""

    answer = request.form.get('answer')
    curr_question_index = len(responses)
    survey_question_count = len(survey.questions)

    if(answer):
        responses.append(answer)
        curr_question_index = len(responses)

        if(curr_question_index == survey_question_count):
            return redirect("/completion")

        return redirect(f"/questions/{curr_question_index}")

    else:
        error = "Please select a choice before continuing"
        return render_template(
        "question.html",
        question=survey.questions[curr_question_index],
        error=error)


@app.get("/completion")
def complete():
    """Return completed survey page"""

    survey_question_count = len(responses)

    return render_template(
                "completion.html",
                question_count=survey_question_count,
                complete_responses=responses,
                questions=survey.questions)

