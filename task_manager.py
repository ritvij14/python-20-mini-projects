import sqlite3

import click


def init_db():
    db = sqlite3.connect("tasks.db")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, completion_status BOOLEAN NOT NULL)"""
    )
    db.commit()
    db.close()


def add_task(title: str, desc: str, completion_status: bool):
    try:
        db = sqlite3.connect("tasks.db")
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO tasks (title, description, completion_status) VALUES (?, ?, ?)""",
            (title, desc, completion_status),
        )
        task_id = cursor.lastrowid
        db.commit()
        db.close()
        return f"Task added successfully with ID: {task_id}"
    except Exception as e:
        return f"Error adding task: {e}"


def view_tasks():
    try:
        db = sqlite3.connect("tasks.db")
        cursor = db.cursor()
        cursor.execute(
            """SELECT * FROM tasks""",
        )
        tasks = cursor.fetchall()
        db.close()
        return tasks
    except Exception as e:
        return f"Error viewing tasks: {e}"


def update_task(task_id: int):
    try:
        db = sqlite3.connect("tasks.db")
        cursor = db.cursor()
        cursor.execute(
            """UPDATE tasks SET completion_status = true WHERE id = ?""",
            (task_id,),
        )
        db.commit()
        db.close()
        return f"Task updated successfully"
    except Exception as e:
        return f"Error updating task: {e}"


def delete_task(task_id: int):
    try:
        db = sqlite3.connect("tasks.db")
        cursor = db.cursor()
        cursor.execute(
            """DELETE FROM tasks WHERE id = ?""",
            (task_id,),
        )
        db.commit()
        db.close()
        return f"Task deleted successfully"
    except Exception as e:
        return f"Error deleting task: {e}"


@click.group()
def cli():
    pass


@cli.command()
@click.option("--title", prompt="Task title", help="Title of the task")
@click.option("--description", prompt="Task description", help="Desription of the task")
def add(title, description):
    result = add_task(title, description, False)
    click.echo(result)


@cli.command()
def view():
    tasks = view_tasks()
    if isinstance(tasks, list):
        for task in tasks:
            click.echo(
                f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Completed: {task[3]}"
            )
    else:
        click.echo(tasks)


@cli.command()
@click.option("--id", prompt="Task ID", help="ID of the task")
def complete(id):
    result = update_task(id)
    click.echo(result)


@cli.command()
@click.option("--id", prompt="Task ID", help="ID of the task")
def delete(id):
    result = delete_task(id)
    click.echo(result)


if __name__ == "__main__":
    init_db()
    cli()
