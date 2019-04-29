from config import app
from controller_functions import home, register, login, dashboard, view_add_trip_page, add_trip, see_view_trip_page, cancel_trip, leave_trip, join_trip, logout

app.add_url_rule("/", view_func=home)
app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/travels", view_func=dashboard, methods=["GET", "POST"])
app.add_url_rule("/travels/add", view_func=view_add_trip_page, methods=["GET", "POST"])
app.add_url_rule("/add_trip", view_func=add_trip, methods=["POST"])
app.add_url_rule("/travels/destination/<id>", view_func=see_view_trip_page, methods=["GET", "POST"])
app.add_url_rule("/cancel_trip", view_func=cancel_trip, methods=["POST"])
app.add_url_rule("/leave_trip", view_func=leave_trip, methods=["POST"])
app.add_url_rule("/join_trip", view_func=join_trip, methods=["POST"])
app.add_url_rule("/logout", view_func=logout, methods=["POST"])
