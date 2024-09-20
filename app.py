from flask import Flask, jsonify, request
from celery import Celery

# Initialize Flask app
app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define a simple Celery task
@celery.task
def add(x, y):
    return x + y

# Define a route to call the task
@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    
    if x is None or y is None:
        return jsonify({'error': 'Please provide both x and y values.'}), 400

    # Call the task asynchronously
    task = add.delay(x, y)
    
    return jsonify({'task_id': task.id}), 202  # Return the task ID

# Define a route to check the task status
@app.route('/task/<task_id>', methods=['GET'])
def task_status(task_id):
    task = add.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}  # Exception details
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
