from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_hours(start, end):
    # Convert start and end times to minutes
    start_minutes = int(start.split(':')[0]) * 60 + int(start.split(':')[1])
    end_minutes = int(end.split(':')[0]) * 60 + int(end.split(':')[1])

    # Calculate total working minutes
    total_minutes = end_minutes - start_minutes

    # Apply break logic
    if total_minutes > 240:  # 4 hours
        total_minutes += 15
    if total_minutes > 480:  # 8 hours
        total_minutes += 30

    # Convert total minutes back to hours and minutes
    total_hours, remainder = divmod(total_minutes, 60)

    return f"{int(total_hours)}:{int(remainder):02d}"

    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        workers = int(request.form['workers'])
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Calculate total hours for all workers
        total_hours = calculate_hours(start_time, end_time) * workers

        return render_template('index.html', total_hours=total_hours)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
