import pytest
import tasks

@pytest.mark.skipif(tasks.__version__ < '0.2.0',
                    reason='not supported until version 0.2.0')
def test_unique_id_1():
    """Calling unique_id() twice should return different numbers."""
    id_1 = tasks.unique_id()
    id_2 = tasks.unique_id()

    assert id_1 != id_2


def test_unique_id_2():
    """unique_id() should return an unused id."""
    ids = []
    ids.append(tasks.add(tasks.Task('one')))
    ids.append(tasks.add(tasks.Task('two')))
    ids.append(tasks.add(tasks.Task('three')))

    # Grab a unique id
    uid = tasks.unique_id()

    # Make sure it isn't the list of existing ids
    assert uid not in ids


@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    # Setup: start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')

    # This is where testing happens
    yield

    # Teardown: stop db
    tasks.stop_tasks_db()
