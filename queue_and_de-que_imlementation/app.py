from flask import Flask, render_template

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0
    
    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty, cannot dequeue.")
        return self.queue.pop(0)
    
    def size(self):
        return len(self.queue)

app = Flask(__name__)

my_queue = Queue()

@app.route('/')
def index():
    return render_template('index.html', queue=my_queue.queue)

@app.route('/enqueue', methods=['POST'])
def enqueue():
    item = request.form.get('item')
    if item:
        my_queue.enqueue(item)
    return redirect(url_for('index'))

@app.route('/dequeue')
def dequeue():
    try:
        my_queue.dequeue()
    except Exception as e:
        print(e)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
