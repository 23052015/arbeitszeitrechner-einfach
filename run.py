import os
from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)


def format_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"


def round_to_nearest_quarter_hour(dt):
    minutes = dt.minute
    rounded_minutes = 15 * round(minutes / 15)
    return dt.replace(minute=rounded_minutes, second=0, microsecond=0)


def calculate_total_hours_and_break(workers, start, end, breakk):
    start_time = round_to_nearest_quarter_hour(datetime.strptime(start, "%H:%M"))
    end_time = round_to_nearest_quarter_hour(datetime.strptime(end, "%H:%M"))
    break_time = round_to_nearest_quarter_hour(datetime.strptime(breakk, "%H:%M"))


    # Calculate total working time for one worker
    total_time_per_worker = end_time - start_time

    # Calculate total working time for all workers
    total_time = total_time_per_worker * workers

    # Convert total_time to hours and minutes
    total_hours, remainder = divmod(int(total_time.total_seconds()), 3600)
    total_minutes = remainder // 60

    # Calculate total break time in seconds
    break_seconds = (break_time - datetime(1900, 1, 1)).total_seconds()

    # Convert break_time to hours and minutes
    break_hours, break_remainder = divmod(int(break_seconds), 3600)
    break_minutes = break_remainder // 60

    return {
        'workers': workers,
        'total_hours': f"{total_hours:02}:{total_minutes:02}",
        'total_break': f"{break_hours:02}:{break_minutes:02}",
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        workers = int(request.form['workers'])
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        break_time = request.form['break_time']

        # Calculate total hours and break for all workers
        result = calculate_total_hours_and_break(workers, start_time, end_time, break_time)

        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
