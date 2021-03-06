from config import app
from controller_functions import home, register, login, dashboard, myaccount, edit_walk, setdefaultpic, changedefaultpic, editaccount, addadog, delete_a_dog, viewdog, add_walk, see_view_walk_page, cancel_walk, leave_walk, join_walk, logout, editdog

app.add_url_rule("/", view_func=home)
app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/dashboard", view_func=dashboard, methods=["GET", "POST"])
app.add_url_rule("/setdefault", view_func=setdefaultpic, methods=["POST"])
app.add_url_rule("/upload_url", view_func=changedefaultpic, methods=["POST"])
app.add_url_rule("/myaccount", view_func=myaccount, methods=["GET", "POST"])
app.add_url_rule("/editaccount", view_func=editaccount, methods=["POST"])
app.add_url_rule("/editdog", view_func=editdog, methods=["POST"]) #this was added
app.add_url_rule("/addadog", view_func=addadog, methods=["POST"])
app.add_url_rule("/delete_a_dog", view_func=delete_a_dog, methods=["POST"])
app.add_url_rule("/dog/<id>", view_func=viewdog, methods=["GET","POST"])
app.add_url_rule("/add_walk", view_func=add_walk, methods=["POST"])
app.add_url_rule("/edit_walk/<id>", view_func=edit_walk, methods=["POST"])
app.add_url_rule("/view_walk/<id>", view_func=see_view_walk_page, methods=["GET", "POST"])
app.add_url_rule("/cancel_walk", view_func=cancel_walk, methods=["POST"])
app.add_url_rule("/leave_walk", view_func=leave_walk, methods=["POST"])
app.add_url_rule("/join_walk", view_func=join_walk, methods=["POST"])
app.add_url_rule("/logout", view_func=logout, methods=["POST"])