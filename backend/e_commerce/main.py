from argparse import ArgumentParser

from process_data import clear_project, init_project, process_transaction

if __name__ == "__main__":
    parser = ArgumentParser("Action to perform on the project")
    parser.add_argument(
        "action_on_project",
        help="Action to perform on th project",
        choices=["init", "clear", "one_transaction"],
        default="clear",
    )
    args = parser.parse_args()
    if args.action_on_project == "init":
        print("Initializing the project")
        init_project()
        print("Database e_commerce and tables are created")
    elif args.action_on_project == "clear":
        print("Clearing the project")
        clear_project()
        print("Database e_commerce and tables are cleared")
    elif args.action_on_project == "one_transaction":
        print("One transaction is performed")
        process_transaction()
        print("The transaction is processed")
