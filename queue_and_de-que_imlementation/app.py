from flask import Flask, render_template, request, redirect, url_for, flash, session
from collections import deque

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
    
    def peek(self):
        if self.is_empty():
            return None
        return self.front.data
    
    def get_queue_list(self):
        """Convert linked list to Python list for display"""
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

Q = Queue()
tabs = deque()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

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
    session.pop('_flashes', None)
    return render_template('restaurant.html', queue=Q.get_queue_list())

@app.route('/projects/restaurant_simulator/add', methods=['POST'])
def add_customer():
    name = request.form.get('name')
    if name:
        Q.enqueue(name)
        flash(f'✅ Added "{name}" to the queue!', 'success')
    else:
        flash('❌ Please enter a customer name!', 'error')
    return redirect(url_for('restaurant'))

@app.route('/projects/restaurant_simulator/remove', methods=['POST'])
def remove_customer():
    if Q.is_empty():
        flash('❌ Queue is empty, nothing to remove!', 'error')
    else:
        removed = Q.dequeue()
        flash(f'✅ Removed "{removed}" from the queue!', 'success')
    return redirect(url_for('restaurant'))

@app.route('/projects/restaurant_simulator/next')
def next_customer():
    next_customer = Q.peek()
    if next_customer is None:
        flash('ℹ️ Queue is empty, no next customer!', 'info')
    else:
        flash(f'👤 Next customer: {next_customer}', 'info')
    return redirect(url_for('restaurant'))

@app.route('/projects/restaurant_simulator/size')
def queue_size():
    size = Q.size()
    flash(f'📊 Queue size: {size} customer(s)', 'info')
    return redirect(url_for('restaurant'))

# Tab Manager Routes
@app.route('/projects/tab_manager')
def tab_manager():
    return render_template('tab_manager.html', tabs=list(tabs))

@app.route('/projects/tab_manager/add_front', methods=['POST'])
def add_front():
    page = request.form.get("page")
    if page:
        tabs.appendleft(page)
        flash(f'✅ Added "{page}" to front!', 'success')
    else:
        flash('❌ Please enter a page name!', 'error')
    return redirect(url_for("tab_manager"))

@app.route('/projects/tab_manager/add_rear', methods=['POST'])
def add_rear():
    page = request.form.get("page")
    if page:
        tabs.append(page)
        flash(f'✅ Added "{page}" to rear!', 'success')
    else:
        flash('❌ Please enter a page name!', 'error')
    return redirect(url_for("tab_manager"))

@app.route('/projects/tab_manager/remove_front', methods=['POST'])
def remove_front():
    if tabs:
        removed = tabs.popleft()
        flash(f'✅ Removed "{removed}" from front!', 'success')
    else:
        flash('❌ No tabs to remove!', 'error')
    return redirect(url_for("tab_manager"))

@app.route('/projects/tab_manager/remove_rear', methods=['POST'])
def remove_rear():
    if tabs:
        removed = tabs.pop()
        flash(f'✅ Removed "{removed}" from rear!', 'success')
    else:
        flash('❌ No tabs to remove!', 'error')
    return redirect(url_for("tab_manager"))

if __name__ == "__main__":
    app.run(debug=True)
