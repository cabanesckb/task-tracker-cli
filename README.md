# Task CLI
A command-line task manager built in Python.

## Usage
```bash
python task_cli.py add "Buy groceries"
python task_cli.py list
python task_cli.py list done
python task_cli.py list in-progress
python task_cli.py update 1 "New description"
python task_cli.py delete 1
python task_cli.py mark-done 1
python task_cli.py mark-in-progress 1
```
## Running tests
```bash
pip install pytest
pytest test_tasks.py
```