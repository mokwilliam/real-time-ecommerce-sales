from argparse import ArgumentParser

from process_data import clear_project, init_project

if __name__ == "__main__":
    parser = ArgumentParser("Action to perform on the project")
    parser.add_argument(
        "action_on_project",
        help="The state of the project (init/clear)",
        choices=["init", "clear"],
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
