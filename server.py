from flask import Flask, url_for, render_template, request, redirect
import repositories
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    questions = repositories.get_last_5_questions()
    if request.args.get("search"):
        search = request.args.get("search")
        return redirect(url_for("search", search_phrase=search))
    return render_template("home.html", questions=questions)


@app.route("/list")
def question_list():
    order_by = "submission_time"
    direction = "DESC"
    if "order_by" in request.args and "direction" in request.args:
        order_by = request.args["order_by"]
        direction = request.args["direction"]
    questions = repositories.get_all_data("question", order_by, direction)

    return render_template(
        "list.html",
        questions=questions,
        order_by=order_by,
        direction=direction,
    )


@app.route("/question/<question_id>")
def display_question_by_id(question_id):
    question = repositories.get_data_by_question_id("question", question_id)[0]
    answers = repositories.get_data_by_question_id("answer", question_id)
    comments = repositories.get_comments()
    tags = repositories.get_question_tags(question_id)
    return render_template("display_question.html", question=question, answers=answers, comments=comments, tags=tags)


@app.route("/search/<search_phrase>", methods=["POST", "GET"])
def search(search_phrase):
    found_data = repositories.search(search_phrase)
    return render_template("search.html", found_data=found_data, search_phrase=search_phrase)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        image = request.form["image"]

        if image == "":
            image = None
        repositories.add_new_question(title, message, image)
        return redirect(url_for("question_list"))
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["POST"])
def add_answer(question_id):
    if request.method == "POST":
        message = request.form["message"]
        image = ""
        repositories.add_new_answer(message, image, question_id)
        return redirect("/question/" + question_id)

    question = repositories.get_data_by_question_id("question", question_id)[0]
    return render_template("add_answer.html", question=question)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    repositories.delete_data(question_id, "question")
    return redirect(url_for("question_list"))


@app.route("/<question_id>/<answer_id>/delete")
def delete_answer(answer_id, question_id):
    repositories.delete_data(answer_id, "answer")
    return redirect(url_for("display_question_by_id", question_id=question_id))


@app.route("/question/<question_id>/edit_a_question", methods=["POST"])
def edit_question(question_id):
    title = request.form["title"]
    message = request.form["message"]
    image = request.form["image"]
    repositories.edit_question("question", question_id, title, message, image)
    return redirect(url_for("display_question_by_id", question_id=question_id))


@app.route("/question/<question_id>/vote_up", methods=["POST"])
def vote_up_question(question_id):
    repositories.register_question_vote(question_id=question_id, vote=1)
    return redirect(url_for("question_list"))


@app.route("/question/<question_id>/vote_down_question", methods=["POST"])
def vote_down_question(question_id):
    repositories.register_question_vote(question_id=question_id, vote=-1)
    return redirect(url_for("question_list"))


@app.route("/question/<question_id>/<answer_id>/vote_up_answer", methods=["POST"])
def vote_up_answer(answer_id, question_id):
    repositories.register_answer_vote(answer_id, question_id, vote=1)
    return redirect(url_for("display_question_by_id", question_id=question_id))


@app.route("/question/<question_id>/<answer_id>/vote_down_answer", methods=["POST"])
def vote_down_answer(answer_id, question_id):
    repositories.register_answer_vote(answer_id, question_id, vote=-1)
    return redirect(url_for("display_question_by_id", question_id=question_id))


@app.route("/question/<question_id>/new_comment", methods=["POST"])
def add_comment_to_question(question_id):
    if request.method == "POST":
        message = request.form["message"]
        repositories.add_comment_question(question_id, message)
        return redirect("/question/" + question_id)
    comment = repositories.get_data_by_question_id("comment", question_id)[0]
    return render_template("add_comment_to_question.html", comment=comment)


@app.route("/answer/<question_id>/<answer_id>/new_comment", methods=["POST"])
def add_comment_to_answer(question_id, answer_id):
    if request.method == "POST":
        message = request.form["message"]
        repositories.add_comment_answer(answer_id, message)
        return redirect("/question/" + question_id)
    comment = repositories.get_data_by_question_id("comment", question_id)[0]
    return render_template("add_comment_to_answer.html", comment=comment)


@app.route("/answer/<question_id>/<answer_id>/edit_answer", methods=["GET", "POST"])
def edit_answer(question_id, answer_id):
    if request.method == "POST":
        message = request.form["message"]
        # image = request.form["image"]
        repositories.edit_answer(answer_id, message)
        return redirect(url_for("display_question_by_id", question_id=question_id))
    return render_template("answer_form.html")

@app.route("/comment/<question_id>/<comment_id>", methods=["GET", "POST"])
def edit_comment(question_id, comment_id):
    if request.method == "POST":
        message = request["message"]
        repositories.edit_comment(comment_id, message)
        return redirect(url_for("display_question_by_id", question_id=question_id))
    return render_template("comment_form.html")

@app.route("/comments/<comment_id>/<question_id>/delete")
def delete_question_comment(comment_id, question_id):
    repositories.delete_data(comment_id, "comment")
    return redirect(url_for("display_question_by_id", question_id=question_id))

@app.route("/comments/<comment_id>/<question_id>/<answer_id>/delete")
def delete_answer_comment(comment_id,question_id, answer_id):
    repositories.delete_data(comment_id, "comment")
    return redirect(url_for("display_question_by_id",question_id=question_id, answer_id=answer_id))


@app.route("/question/<question_id>/new-tag", methods=["POST"])
def add_tag(question_id):
    if request.method == "POST":
        name = request.form["name"]
        tag_id = repositories.add_tag(name)
        repositories.update_question_tag_table(question_id, tag_id)
        return redirect("/question/" + question_id)

    question = repositories.get_data_by_question_id("question", question_id)[0]
    return render_template("tag.html", question=question)


if __name__ == "__main__":
    app.run(port=4000, debug=True)
