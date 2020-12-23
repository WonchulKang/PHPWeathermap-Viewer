from flask import Flask, jsonify, render_template, request, abort
import os, glob, datetime

from app import config

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title=config.TITLE, map_data=config.MAP_DATA, base_url=config.MAP_BASE_URL)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title=config.TITLE)


def get_prev(c_time):
    first_dir = sorted(glob.glob(config.IMAGE_PATH + "/*"))[0]
    first_file = sorted(glob.glob(first_dir + "/*.png"))[0]
    first_time_obj = datetime.datetime.strptime(os.path.basename(first_file), "%Y-%m-%d_%H:%M.png")

    temp_time_obj = c_time
    while True:
        temp_time_obj = temp_time_obj - datetime.timedelta(minutes=1)
        new_path = temp_time_obj.strftime("/%Y-%m-%d/%Y-%m-%d_%H:%M.png")
        if os.path.exists(config.IMAGE_PATH + new_path):
            return { 'year'     : "%04d" % temp_time_obj.year, \
                     'month'    : "%02d" % temp_time_obj.month, \
                     'day'      : "%02d" % temp_time_obj.day, \
                     'hour'     : "%02d" % temp_time_obj.hour, \
                     'minute'   : "%02d" % temp_time_obj.minute }
        if first_time_obj > temp_time_obj:
            return None

def get_next(c_time):
    last_dir = sorted(glob.glob(config.IMAGE_PATH + "/*"))[-1]
    last_file = sorted(glob.glob(last_dir + "/*.png"))[-1]
    last_time_obj = datetime.datetime.strptime(os.path.basename(last_file), "%Y-%m-%d_%H:%M.png")

    temp_time_obj = c_time
    while True:
        temp_time_obj = temp_time_obj + datetime.timedelta(minutes=1)
        new_path = temp_time_obj.strftime("/%Y-%m-%d/%Y-%m-%d_%H:%M.png")
        if os.path.exists(config.IMAGE_PATH + new_path):
            return { 'year'     : "%04d" % temp_time_obj.year, \
                     'month'    : "%02d" % temp_time_obj.month, \
                     'day'      : "%02d" % temp_time_obj.day, \
                     'hour'     : "%02d" % temp_time_obj.hour, \
                     'minute'   : "%02d" % temp_time_obj.minute }
        if last_time_obj < temp_time_obj:
            return None
        

@app.route("/data/image")
def get_image():
    if not request.args.get("year"):
        last_dir = sorted(glob.glob(config.IMAGE_PATH + "/*"))[-1]
        last_file = sorted(glob.glob(last_dir + "/*.png"))[-1]
        current_date_time_obj = datetime.datetime.strptime(os.path.basename(last_file), "%Y-%m-%d_%H:%M.png")
        re_filename = "/static/image/" + os.path.basename(last_dir) + "/" + os.path.basename(last_file)
        return jsonify(filename=re_filename, prev=get_prev(current_date_time_obj))
    else:
        year = request.args.get("year")
        month = request.args.get("month")
        day = request.args.get("day")
        hour = request.args.get("hour")
        minute = request.args.get("min")
        
        filename = "/%s-%s-%s/%s-%s-%s_%s:%s.png" % (year, month, day, year, month, day, hour, minute)
        current_date_time_obj = datetime.datetime.strptime(os.path.basename(filename), "%Y-%m-%d_%H:%M.png")


        if os.path.exists(config.IMAGE_PATH + filename):
            return jsonify(filename="/static/image" + filename, prev=get_prev(current_date_time_obj), next=get_next(current_date_time_obj))
        else:
            abort(404);
            
@app.route("/data")
def get_all_year():
    year_list = []
    for item in glob.glob(config.IMAGE_PATH + "/*"):
        year_item = os.path.basename(item).split("-")[0]
        if year_item not in year_list:
            year_list.append(year_item)

    year_list = sorted(year_list)

    return jsonify(year=year_list)
        

@app.route("/data/<year_string>")
def get_all_month(year_string):
    month_list = []
    for item in glob.glob(config.IMAGE_PATH + "/%s-*" % year_string):
        month_item = os.path.basename(item).split("-")[1]
        if month_item not in month_list:
            month_list.append(month_item)

    month_list = sorted(month_list)

    return jsonify(month=month_list)

@app.route("/data/<year_string>/<month_string>")
def get_all_day(year_string, month_string):
    day_list = []
    for item in glob.glob(config.IMAGE_PATH + "/%s-%s-*" % (year_string, month_string)):
        day_item = os.path.basename(item).split("-")[2]
        if day_item not in day_list:
            day_list.append(day_item)

    day_list = sorted(day_list)

    return jsonify(day=day_list)

@app.route("/data/<year_string>/<month_string>/<day_string>")
def get_all_hour(year_string, month_string, day_string):
    hour_list = []
    for item in glob.glob(config.IMAGE_PATH + "/%s-%s-%s/*.png" % (year_string, month_string, day_string)):
        hour_item = os.path.basename(item).split("_")[1].split(":")[0]
        if hour_item not in hour_list:
            hour_list.append(hour_item)

    hour_list = sorted(hour_list)

    return jsonify(hour=hour_list)


@app.route("/data/<year_string>/<month_string>/<day_string>/<hour_string>")
def get_all_min(year_string, month_string, day_string, hour_string):
    min_list = []
    for item in glob.glob(config.IMAGE_PATH + "/%s-%s-%s/*_%s*.png" % (year_string, month_string, day_string, hour_string)):
        min_item = os.path.basename(item).split("_")[1].split(":")[1].split(".")[0]
        if min_item not in min_list:
            min_list.append(min_item)

    min_list = sorted(min_list)

    return jsonify(minute=min_list)
