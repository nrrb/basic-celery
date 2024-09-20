# Testing Celery + redis + Flask

The simplest example possible to test your Celery and redis setup. 

Make sure [redis-server](https://redis.io/) is installed. For the Mac:

```bash
brew install redis
```

Set up your Python3 virtual environment:

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` is very simple, it contains only three libraries ([Flask](https://pypi.org/project/Flask/), [celery](https://pypi.org/project/celery/), [redis](https://pypi.org/project/redis/)):

```
celery==5.4.0
Flask==3.0.3
redis==5.0.8
```

Run `redis-server`:

```bash
redis-server
```

Run the Flask app:

```bash
python app.py
```

Run a Celery worker:

```bash
celery -A app.celery worker --loglevel=info
```

Submit a task to the Flask app using curl:

```bash
curl -X POST http://127.0.0.1:5000/add -H "Content-Type: application/json" -d '{"x": 5, "y": 7}'
```

You'll get output back looking something like this:

```json
{
  "task_id": "f23924fe-9fda-4d60-8aa7-a739c1dfd0ed"
}
```

Using the `task_id` from the output, substitute it into this command and run it to check on the task status:

```bash
curl http://127.0.0.1:5000/task/f23924fe-9fda-4d60-8aa7-a739c1dfd0ed
```


If both `redis-server` and the Celery worker are running, you should get back output like this:

```json
{
  "result": 12,
  "state": "SUCCESS"
}
```

## Troubleshooting

When you check the status and you don't see the result, it may be due to your Celery worker is not running. Since the task in this example is extremely simple, it should return almost immediately. If you check task status and you see the following, make sure the Celery worker is running:

```
{
  "state": "PENDING",
  "status": "Pending..."
}
```
You can clear out all Celery cache and redis data by running:

```
celery -A app.celery purge
redis-cli flushall
```

You can also do this through running the `clear_celery.sh` command in this repo. 
