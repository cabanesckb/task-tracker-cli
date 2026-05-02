import os
import sys
import json
import datetime

def main():
    try:
        handle_cmd()
    except IndexError as e:
        print("usage: [add|update|delete|list]")
    except ValueError as e:
        print(e)


def id_gen(tasks):
    """Return the next available task ID."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


# Add task
def create_task(task_id, description, now=None):
    """Return a new task dict with the given ID, description, and todo status."""
    now = now if now is not None else datetime.datetime.now().isoformat()
    return {
            'id': task_id,
            'description': description,
            'status': 'todo',
            'created_at': now,
            'updated_at': now,
        }


def load_tasks():
    """Load and return tasks from tasks.json, or an empty list if the file doesn't exist."""
    if os.path.exists('tasks.json'):
        with open('tasks.json') as f:
            tasks = json.load(f)
    else:
        tasks = []
    return tasks


def save_tasks(tasks):
    """Save tasks in tasks.json."""
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=2)


def add_task():
    if len(sys.argv) != 3:
        print('usage: add <"description">')
        return
    
    tasks = load_tasks()
    task = create_task(id_gen(tasks), sys.argv[2])
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID:{task['id']})")


# Update tasks
def apply_update(tasks, target_id, new_description):
    """Update a task's description by ID and return (task, tasks), or (None, tasks) if not found."""
    task = next((task for task in tasks if task['id'] == target_id), None)
    
    if task is None:
        return None, tasks
    
    task['description'] = new_description
    task['updated_at'] = datetime.datetime.now().isoformat()
    
    return task, tasks


def update_task():
    if len(sys.argv) != 4:
        print('usage: update <id> <"new description">')
        return
    
    tasks = load_tasks()
    target_id = int(sys.argv[2])
    new_description = sys.argv[3]
    
    task, updated_tasks = apply_update(tasks, target_id, new_description)
    
    if task is None:
        print(f"No task found with ID: {target_id}")
        return
    
    save_tasks(updated_tasks)
    
    print(f"Task updated successfully (ID:{target_id})")


def apply_status(tasks, target_id, new_status):
    """Update a task's status by ID and return (task, tasks), or (None, tasks) if not found."""
    task = next((task for task in tasks if task['id'] == target_id), None)
    
    if task is None:
        return None, tasks
    
    task['status'] = new_status
    task['updated_at'] = datetime.datetime.now().isoformat()
    
    return task, tasks


def update_status(target_id, new_status):
    tasks = load_tasks()
    
    task, updated_tasks = apply_status(tasks, int(target_id), new_status)
    
    if task is None:
        print(f"No task found with ID: {target_id}")
        return
    
    save_tasks(updated_tasks)
    
    print(f"Task mark-{new_status} (ID:{target_id})")


def mark_in_progress():
    if len(sys.argv) != 3:
        print("Usage: mark-in-progress <id>")
        return
    
    target_id = sys.argv[2]
    update_status(target_id, 'in-progress')


def mark_done():
    if len(sys.argv) != 3:
        print("Usage: mark-done <id>")
        return
    
    target_id = sys.argv[2]
    update_status(target_id, 'done')


# Delete task
def apply_delete(tasks, target_id):
    """Remove a task by ID and return (new_tasks, found) where found is a bool."""
    original_count = len(tasks)
    new_tasks = [task for task in tasks if task['id'] != target_id]
    
    found = len(new_tasks) != original_count
    return new_tasks, found


def delete_task():
    if len(sys.argv) != 3:
        print("Usage: delete_task <id>")
        return
    
    tasks = load_tasks()
    target_id = int(sys.argv[2])
    
    new_tasks, found = apply_delete(tasks, target_id)
    
    if not found:
        print(f"Task with an ID:{target_id} was not found.")
        return
    
    save_tasks(new_tasks)
    
    print(f"Task deleted successfully (ID:{target_id})")


# List tasks
def list_task():
    if len(sys.argv) > 3:
        print('usage: list | list done | list in-progress')
        return
    
    tasks = load_tasks()
    
    if not tasks:
        print("No task found.")
        return
    
    print(f"{'ID':<15} {'Description':<30} {'updated'}")
    print('-' * 70)
    
    status = sys.argv[2] if len(sys.argv) == 3 else None
    
    filtered_tasks = [task for task in tasks if task['status'] == status] if status else tasks
    
    for task in filtered_tasks:
        updated = datetime.datetime.fromisoformat(task['updated_at']).strftime("%b %d, %Y %I:%M %p")
        print(f"{task['id']:<15} {task['description']:<30} {updated}")


OPERATIONS = {'add': add_task, 
              'update': update_task, 
              'delete': delete_task, 'list': list_task, 
              'mark-in-progress': mark_in_progress,
              'mark-done':mark_done}


def handle_cmd():
    action = sys.argv[1].lower()
    fn = OPERATIONS.get(action)
    if not fn:
        raise ValueError("Unknown action should be [add|update|delete|list]")
    return fn()


if __name__ == '__main__':
    main()