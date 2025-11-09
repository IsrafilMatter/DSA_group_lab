from flask import Flask, render_template, request, redirect, url_for

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def is_empty(self):
        return self.front is None
    
    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty, cannot dequeue.")
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return temp.data
    
    def size(self):
        return self._size
    
    def get_queue_list(self):
        """Convert linked list to Python list for display"""
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

Q = Queue()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profiles.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/projects/restaurant_simulator')
def restaurant():
    return render_template('restaurant.html', queue=Q.get_queue_list())

@app.route('/projects/restaurant_simulator/add', methods=['POST'])
def add_customer():
    name = request.form.get('name')
    if name:
        Q.enqueue(name)
    return redirect(url_for('restaurant'))

@app.route('/projects/restaurant_simulator/next')
def next_customer():
    if Q.is_empty():
        return "Queue is empty, no next customer."
    return f"Next customer: {Q.front.data}"

@app.route('/projects/restaurant_simulator/size')
def queue_size():
    return f"Queue size: {Q.size()}"

@app.route('/projects/restaurant_simulator/remove')
def remove_customer():
    if Q.is_empty():
        return "Queue is empty, nothing to remove."
    removed = Q.dequeue()
    return f"Removed '{removed}' from queue."

@app.route('/projects/restaurant_simulator/queue')
def view_queue():
    return f"Current queue: {Q.get_queue_list()}"

if __name__ == "__main__":
    app.run(debug=True)