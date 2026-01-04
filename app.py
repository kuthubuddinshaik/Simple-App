from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    """Create the tasks table if it doesn't exist"""
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, completed FROM tasks')
    tasks = [{'id': row[0], 'name': row[1], 'completed': bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return tasks

def add_task(name):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def toggle_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END
        WHERE id = ?
    ''', (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# --- Initialize DB ---
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_name = request.form.get('task')
        if task_name:
            add_task(task_name)
        return redirect(url_for('index'))
    
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    toggle_task(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
