from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def show_surveys():
    """Shows a list of available surveys"""

    return render_template('survey_list.html',
                           surveys=surveys)

@app.get("/<survey_code>")
def survey_start(survey_code):
    """Returns the start survey page"""

    session[survey_code] = []

    return render_template(
        "survey_start.html",
        survey_code=survey_code,
        survey=surveys[survey_code])


@app.post("/<survey_code>/begin")
def begin(survey_code):
    """Redirects to start survey"""

    return redirect(f"/{survey_code}/questions/0")


@app.get("/<survey_code>/questions/<int:question_num>")
def show_question(survey_code, question_num):
    """Returns question number question_num"""

    num_of_responses = len(session[survey_code])

    if num_of_responses == question_num:
        return render_template(
            "question.html",
            survey_code=survey_code,
            question=surveys[survey_code].questions[question_num])

    elif num_of_responses == len(surveys[survey_code].questions):
        flash("You've already completed the survey!")
        return redirect(f"/{survey_code}/completion")

    else:
        flash(f"You haven't answered question { num_of_responses }")
        return redirect(f"/{survey_code}/questions/{ num_of_responses }")



@app.post("/<survey_code>/answer")
def handle_answer(survey_code):
    """Store answer locally and redirect to next question"""

    answer = request.form.get('answer')
    curr_question_index = len(session[survey_code])
    survey_question_count = len(surveys[survey_code].questions)

    if(answer):
        responses = session[survey_code]
        responses.append(answer)
        session[survey_code] = responses

        curr_question_index = len(session[survey_code])

        if(curr_question_index == survey_question_count):
            return redirect(f"/{survey_code}/completion")

        return redirect(f"/{survey_code}/questions/{curr_question_index}")

    else:
        flash("Please select a choice before continuing")

        return redirect(f"/{survey_code}/questions/{curr_question_index}")


@app.get("/<survey_code>/completion")
def complete(survey_code):
    """Return completed survey page"""

    survey_question_count = len(session[survey_code])

    return render_template(
                "completion.html",
                question_count=survey_question_count,
                survey_code=survey_code,
                questions=surveys[survey_code].questions)



