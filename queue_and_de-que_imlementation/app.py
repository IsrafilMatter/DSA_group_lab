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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profiles.html')

@app.route('/projects')
def works():
    return render_template('projects.html')

if __name__ == "__main__":
    app.run(debug=True)