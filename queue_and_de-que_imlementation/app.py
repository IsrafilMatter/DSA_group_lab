from flask import Flask, render_template, request, redirect, url_for, flash, session
from collections import deque
from bst import BST
from restaurant import Restaurant
import subprocess
import os
import sys

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

restaurant = Restaurant()
tabs = deque()
bst_tree = BST()

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
def restaurant_route():
    session.pop('_flashes', None)
    status = restaurant.status()
    queue = status.get('queue', [])
    return render_template('restaurant.html', 
                         queue=queue,
                         available_tables=status.get('available_tables', {}))

@app.route('/projects/restaurant_simulator/add', methods=['POST'])
def add_customer():
    name = request.form.get('name')
    party_size = request.form.get('party_size', type=int)
    if name and party_size:
        if party_size not in [2, 4, 8]:
            flash('Party size must be 2, 4, or 8!', 'error')
        else:
            message = restaurant.walk_in(name, party_size)
            flash(f'{message}', 'success')
    else:
        flash('Please enter a customer name and party size!', 'error')
    return redirect(url_for('restaurant_route'))

@app.route('/projects/restaurant_simulator/remove', methods=['POST'])
def remove_customer():
    name = request.form.get('name')
    if name:
        message = restaurant.cancel_customer(name)
        flash(f'{message}', 'success')
    else:
        flash('Please enter a customer name!', 'error')
    return redirect(url_for('restaurant_route'))

@app.route('/projects/restaurant_simulator/finish_meal', methods=['POST'])
def finish_meal():
    table_id = request.form.get('table_id', type=int)
    if table_id:
        table_size = table_id // 10
        message = restaurant.finish_meal(table_size, table_id)
        flash(f'{message}', 'success')
    else:
        flash('Please select a table!', 'error')
    return redirect(url_for('restaurant_route'))

# Tab Manager Routes
@app.route('/projects/tab_manager')
def tab_manager():
    return render_template('tab_manager.html', tabs=list(tabs))

@app.route('/projects/tab_manager/add_front', methods=['POST'])
def add_front():
    page = request.form.get("page")
    if page:
        tabs.appendleft(page)
        flash(f'Added "{page}" to front!', 'success')
    else:
        flash('Please enter a page name!', 'error')
    return redirect(url_for("tab_manager"))

@app.route('/projects/tab_manager/add_rear', methods=['POST'])
def add_rear():
    page = request.form.get("page")
    if page:
        tabs.append(page)
        flash(f'Added "{page}" to rear!', 'success')
    else:
        flash('Please enter a page name!', 'error')
    return redirect(url_for("tab_manager"))

@app.route('/projects/tab_manager/remove_front', methods=['POST'])
def remove_front():
    if tabs:
        removed = tabs.popleft()
        flash(f'Removed "{removed}" from front!', 'success')
    else:
        flash('No tabs to remove!', 'error')
    return redirect(url_for("tab_manager"))

@app.route('/projects/tab_manager/remove_rear', methods=['POST'])
def remove_rear():
    if tabs:
        removed = tabs.pop()
        flash(f'Removed "{removed}" from rear!', 'success')
    else:
        flash('No tabs to remove!', 'error')
    return redirect(url_for("tab_manager"))

# Binary Search Tree Routes
@app.route('/projects/binary_tree')
def binary_tree():
    session.pop('_flashes', None)
    nodes, edges, svg_info = bst_tree.layout()
    traversal = bst_tree.post_traversal(bst_tree.root, [])
    return render_template('binary_tree.html', nodes=nodes, edges=edges, svg_info=svg_info, traversal=traversal)

@app.route('/projects/binary_tree/insert', methods=['POST'])
def bst_insert():
    try:
        value = int(request.form.get('value'))
        bst_tree.insert(value)
        flash(f'Inserted {value} into the tree!', 'success')
    except ValueError:
        flash('Please enter a valid number!', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('binary_tree'))

@app.route('/projects/binary_tree/search', methods=['POST'])
def bst_search():
    try:
        value = int(request.form.get('value'))
        found = bst_tree.search(bst_tree.root, value)
        if found:
            flash(f'Found {value} in the tree!', 'success')
        else:
            flash(f'{value} not found in the tree.', 'info')
    except ValueError:
        flash('Please enter a valid number!', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('binary_tree'))

@app.route('/projects/binary_tree/delete', methods=['POST'])
def bst_delete():
    try:
        value = int(request.form.get('value'))
        found = bst_tree.search(bst_tree.root, value)
        if found:
            bst_tree.root = bst_tree.delete_node(bst_tree.root, value)
            flash(f'Deleted {value} from the tree!', 'success')
        else:
            flash(f'{value} not found in the tree.', 'info')
    except ValueError:
        flash('Please enter a valid number!', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('binary_tree'))

@app.route('/projects/binary_tree/clear', methods=['POST'])
def bst_clear():
    bst_tree.root = None
    flash('Tree cleared!', 'success')
    return redirect(url_for('binary_tree'))

# Baccarat Game Routes
@app.route('/projects/baccarat_game')
def baccarat_game():
    session.pop('_flashes', None)
    return render_template('baccarat_game.html')

@app.route('/projects/baccarat_game/run', methods=['POST'])
def run_baccarat_game():
    try:
        # First, check if pygame is installed
        try:
            import pygame
        except ImportError:
            flash('Error: Pygame is not installed. Please install it with: pip install pygame', 'error')
            return redirect(url_for('baccarat_game'))
        
        # Path to the baccarat game script
        # app.py is at: queue_and_de-que_imlementation/app.py
        # baccarat_game.py is at: queue_and_de-que_imlementation/baccarat_game/baccarat_game.py
        current_dir = os.path.dirname(os.path.abspath(__file__))  # queue_and_de-que_imlementation
        game_dir = os.path.join(current_dir, 'baccarat_game')
        script_path = os.path.join(game_dir, 'baccarat_game.py')
        
        # Normalize paths for Windows
        script_path = os.path.normpath(script_path)
        game_dir = os.path.normpath(game_dir)
        
        # Verify the file exists
        if not os.path.exists(script_path):
            flash(f'Error: Game file not found at {script_path}', 'error')
            return redirect(url_for('baccarat_game'))
        
        # Use sys.executable to use the same Python interpreter, or try 'py' as fallback on Windows
        python_exe = sys.executable
        if os.name == 'nt':
            # On Windows, try 'py' launcher if sys.executable doesn't exist
            if not os.path.exists(python_exe):
                python_exe = 'py'
        
        # Debug: Print what we're trying to run
        print(f"Launching game with: {python_exe} {script_path}")
        print(f"Working directory: {game_dir}")
        
        # Launch the game as a subprocess (non-blocking)
        # Set working directory to game directory so assets can be found
        if os.name == 'nt':
            # Windows: Create new console window
            try:
                # Try with CREATE_NEW_CONSOLE first
                process = subprocess.Popen(
                    [python_exe, script_path], 
                    cwd=game_dir,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Give it a moment to start
                import time
                time.sleep(0.5)
                # Check if process is still running (if it crashed immediately)
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    error_msg = stderr.decode('utf-8', errors='ignore') if stderr else 'Unknown error'
                    # Check for common errors
                    if 'ModuleNotFoundError' in error_msg or 'No module named' in error_msg:
                        if 'pygame' in error_msg.lower():
                            flash('Error: Pygame is not installed. Please install it with: pip install pygame', 'error')
                        else:
                            flash(f'Missing module: {error_msg[:150]}', 'error')
                    else:
                        flash(f'Game failed to start: {error_msg[:200]}', 'error')
                    print(f"Game process exited with code {process.returncode}")
                    print(f"STDERR: {error_msg}")
                    return redirect(url_for('baccarat_game'))
            except Exception as e:
                # Fallback: try without CREATE_NEW_CONSOLE
                try:
                    process = subprocess.Popen(
                        [python_exe, script_path], 
                        cwd=game_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    import time
                    time.sleep(0.5)
                    if process.poll() is not None:
                        stdout, stderr = process.communicate()
                        error_msg = stderr.decode('utf-8', errors='ignore') if stderr else 'Unknown error'
                        if 'ModuleNotFoundError' in error_msg or 'No module named' in error_msg:
                            if 'pygame' in error_msg.lower():
                                flash('Error: Pygame is not installed. Please install it with: pip install pygame', 'error')
                            else:
                                flash(f'Missing module: {error_msg[:150]}', 'error')
                        else:
                            flash(f'Game failed to start: {error_msg[:200]}', 'error')
                        return redirect(url_for('baccarat_game'))
                except Exception as e2:
                    flash(f'Error launching game: {str(e2)}', 'error')
                    print(f"Error details: {e2}")
                    import traceback
                    print(traceback.format_exc())
                    return redirect(url_for('baccarat_game'))
        else:
            # Unix/Linux: Run in background
            subprocess.Popen([python_exe, script_path], cwd=game_dir)
        
        flash('Baccarat game launched!', 'success')
    except Exception as e:
        flash(f'Error launching game: {str(e)}', 'error')
        import traceback
        print(f"Error details: {traceback.format_exc()}")
    
    return redirect(url_for('baccarat_game'))

if __name__ == "__main__":
    app.run(debug=True)
