from app.task_controller.task import Task
import argparse
from logger.logging_config import setup_logging



# Set up logging configuration
setup_logging()

def commandline_parser():
    parser = argparse.ArgumentParser(description="Task Manager - Manage your tasks with various commands.")
    parser.add_argument("command", choices=["migrate_table", "view_all", "add", "find", "find_by_id", "update", "delete"], help="Command to execute")
    parser.add_argument("-k", "--keyword", help="Keyword to find tasks by description or status Note: For keyword containing space kindly put them in quotes")
    parser.add_argument("-d", "--description", help="Description of the task Note: For description containing space kindly put them in quotes")
    parser.add_argument("-s", "--status", choices=["pending", "ongoing", "completed"], help="Status of the task")
    parser.add_argument("--id", type=int, help="Task ID for show, update or delete specific task")

    return  parser.parse_args()

def main():
    arguments = commandline_parser()
    match arguments.command:
        case "migrate_table":
            Task().create_table()

        case "view_all":
            Task().tasks()

        case "add":
            Task().create(arguments.description, arguments.status)

        case "find":
            Task().find(arguments.keyword)

        case "find_by_id":
            Task().find_by_id(arguments.id)

        case "update":
            Task().update(arguments.id, arguments.description, arguments.status)

        case "delete":
            Task().delete(arguments.id)

        case _:
            raise ValueError("Not a valid command line argument")

if __name__ == '__main__':
    main()