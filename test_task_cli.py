import pytest
from task_cli import apply_delete, apply_status, apply_update, id_gen, create_task


@pytest.fixture
def sample_tasks():
    return [
        {'id': 1, 'description': 'old', 'status': 'todo', 'updated_at': '2024-01-01'},
        {'id': 2, 'description': 'old', 'status': 'todo', 'updated_at': '2024-01-01'},
    ]

def test_id_gen_empty():
    assert id_gen([]) == 1


def test_id_gen_exist():
    assert id_gen([{'id': 1}, {'id': 2}, {'id': 3}]) == 4


def test_create_task():
    task = create_task(1, 'Buy groceries')
    assert task['id'] == 1
    assert task['description'] == 'Buy groceries'
    assert task['status'] == 'todo'
    assert task['created_at'] == task['updated_at']


def test_apply_update_not_found(sample_tasks):
    task, _ = apply_update(sample_tasks, 99, 'New description')
    assert task is None


def test_apply_update_found(sample_tasks):
    task, _ = apply_update(sample_tasks, 1, 'New description')
    assert task is not None
    assert task['description'] == 'New description'


def test_apply_status_not_found(sample_tasks):
    task, _ = apply_status(sample_tasks, 99, 'done')
    assert task is None


def test_apply_status_found_in_progress(sample_tasks):
    task, _ = apply_status(sample_tasks, 1, 'in-progress')
    assert task is not None
    assert task['status'] == 'in-progress'


def test_apply_status_found_done(sample_tasks):
    task, _ = apply_status(sample_tasks, 1, 'done')
    assert task is not None
    assert task['status'] == 'done'


def test_apply_delete_not_found(sample_tasks):
    _, found = apply_delete(sample_tasks, 99)
    assert not found


def test_apply_delete_last_task():
    tasks = [{'id': 1, 'description': 'old', 'updated_at': '2024-01-01'}]
    new_tasks, found = apply_delete(tasks, 1)
    assert found
    assert new_tasks == []


def test_apply_delete_found_multiple(sample_tasks):
    new_tasks, found = apply_delete(sample_tasks, 1)
    assert found
    assert len(new_tasks) == 1
    assert new_tasks[0]['id'] == 2