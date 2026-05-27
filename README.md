# Discord common server retriever

A (very bad and innefficient) way to retrieve any person with a common server with you

## Running

- Clone this repo
- Install python packages in `requirements.txt` (I used [uv](https://docs.astral.sh/uv/) for this project)
- Create a `.env` file
- Add your personnal Discord Token to it in the form `TOKEN = "you_token_here"`
- First, run `main.py` to create a csv file containing all members of your servers
- Then run `csv_to_sql.py` to create an SQL database that gets queryed right away (this is the part where it gets REALLY weird)

> [!warning] **CAUTION : Automating your Discord account is against ToS and can result in a ban**
>
> I personnally have run it on my 90 servers list and haven't been ban despite already having been warn several times for account automation but still... be carefull, it spams A LOT the API