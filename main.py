import inquirer as inq
import src.discord_client as discord
from src.database_manager import DataBaseManager
from src.utils import TOKEN, console

from os import path

answer = {}
csv_path = None
db_path = None

if path.exists("./data/data.csv") or path.exists("./data/data.db"):
    question = [
        inq.Confirm(
            "overwrite", message="File data.csv or data.db already exists, overwrite ?"
        ),
        inq.Confirm("run_scrapper", message="Run Discord scrapper ?"),
    ]
    answer = inq.prompt(questions=question)

if not answer["overwrite"]:
    file_exists = True
    while file_exists:
        question = [inq.Path("save_path", message="New file name")]
        relative_save_path = inq.prompt(questions=question)["save_path"]
        csv_path = path.abspath(path.join("data/", f"{relative_save_path}.csv"))
        db_path = path.abspath(path.join("data/", f"{relative_save_path}.db"))

        if path.exists(csv_path):
            console.warning(f"File {csv_path} already exists")
        if path.exists(db_path):
            console.warning(f"File {db_path} already exists")
        else:
            file_exists = False
    if str(relative_save_path).endswith(".csv"):
        console.warning("File will have .csv.csv and .csv.db extension")

    with open(str(csv_path), "w") as fp:
        pass
    with open(str(db_path), "w") as fp:
        pass

if answer["run_scrapper"]:
    console.debug("Running Discord client")
    client = discord.MyClient(csv_path)
    try:
        client.run(TOKEN)
    except SystemExit:
        console.debug("Discord scrapper exited")
    except Exception as err:
        console.error(f"Error {str(err)} during scrapper")
        console.error(f"{err.__cause__}")

db = DataBaseManager(csv_path, db_path)
db.feed_db()
print(db.get_members())
