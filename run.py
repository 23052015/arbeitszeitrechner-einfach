from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

def calculate_total_hours_and_break(workers, start, end):
    start_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")

    # Calculate total working time for one worker
    total_time_per_worker = end_time - start_time

    # Apply break logic
    break_time = timedelta(minutes=0)
    if total_time_per_worker >= timedelta(hours=4):
        break_time += timedelta(minutes=15)
    if total_time_per_worker >= timedelta(hours=8):
        break_time += timedelta(minutes=15)

        

    # Calculate total working time for all workers
    total_time = total_time_per_worker * workers

    # Calculate total break time for all workers
    total_break_time = break_time * workers

    total_working_time = total_time - total_break_time

    return {
        'workers': workers,
        'total_hours': str(total_time),
        'total_break': str(total_break_time),
        'total_working_hours': str(total_working_time)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        workers = int(request.form['workers'])
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Calculate total hours and break for all workers
        result = calculate_total_hours_and_break(workers, start_time, end_time)

        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
