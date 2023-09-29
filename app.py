from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def show_surveys():
    """Shows a list of available surveys"""

    return render_template(
        'survey_list.html',
        surveys=surveys)


@app.get("/<survey_code>")
def survey_start(survey_code):
    """Returns the start survey page"""

    return render_template(
        "survey_start.html",
        survey_code=survey_code,
        survey=surveys[survey_code])


# @app.get("/cookie")
# def cookie():
#     html = render_template("completion.html")
#     resp = make_response(redirect(f"/completion")) #am i going to return html?
#     print("resp-----------------------" ,resp)
#     resp.set_cookie(session['curr_survey'], True, max_age=None)
#     return resp



@app.get("/completion")
def complete():
    """Return completed survey page"""
    survey_code = session['curr_survey']
    survey_question_count = len(session[survey_code])

    html = render_template(
        "completion.html",
        question_count=survey_question_count,
        survey_code=survey_code,
        questions=surveys[survey_code].questions)

    resp = make_response(html)

    resp.set_cookie(session['curr_survey'], 'yes', max_age=None)

    return resp
    #TODO: Create logic for the created cookie




@app.post("/<survey_code>/begin")
def begin(survey_code):
    """Redirects to start survey"""

    session[survey_code] = []
    session['curr_survey'] = f"{survey_code}"

    if request.cookies.get(session['curr_survey']):
        return redirect("/complete")

    return redirect(f"/questions/0")


@app.get("/questions/<int:question_num>")
def show_question(question_num):
    """Returns question number question_num"""

    survey_code = session['curr_survey']
    num_of_responses = len(session[survey_code])

    if num_of_responses == len(surveys[survey_code].questions):
        flash("You've already completed the survey!")
        return redirect(f"/completion")
    elif num_of_responses != question_num:
        flash(f"You haven't answered question { num_of_responses }")
        return redirect(f"/questions/{ num_of_responses }")

    return render_template(
            "question.html",
            survey_code=survey_code,
            question=surveys[survey_code].questions[question_num])



@app.post("/answer")
def handle_answer():
    """Store answer locally and redirect to next question"""

    survey_code = session['curr_survey']
    answer = request.form.get('answer', "No answer given")
    comment = request.form.get('comment')
    curr_question_index = len(session[survey_code])
    survey_question_count = len(surveys[survey_code].questions)
    question = surveys[survey_code].questions[curr_question_index]

    if(curr_question_index == survey_question_count):
        return redirect(f"/completion")

    responses = session[survey_code]
    responses.append([answer, comment]) if question.allow_text else responses.append(answer)
    session[survey_code] = responses

    curr_question_index = len(session[survey_code])

    return redirect(f"/questions/{curr_question_index}")



# @app.get("/completion")
# def complete():
#     """Return completed survey page"""
#     survey_code = session['curr_survey']
#     survey_question_count = len(session[survey_code])

#     return render_template(
#         "completion.html",
#         question_count=survey_question_count,
#         survey_code=survey_code,
#         questions=surveys[survey_code].questions)



