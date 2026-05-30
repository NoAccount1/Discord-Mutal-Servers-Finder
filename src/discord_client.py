import os
import pandas as pd
import discord
from discord.abc import Snowflake

if __name__ == "__main__":
    from utils import DEFAULT_CSV_PATH, get_token, console
else:
    from .utils import DEFAULT_CSV_PATH, get_token, console # ty:ignore[unresolved-import]


class MyClient(discord.Client):
    df = pd.DataFrame()
    csv_path: str

    def __init__(self, csv_path=DEFAULT_CSV_PATH):
        self.csv_path = os.path.abspath(csv_path)
        console.debug(f"csv_path is {self.csv_path}")

    async def on_ready(self):
        console.info("Logged on as", self.user)
        console.info("Guild number :", len(self.guilds))
        for guild in self.guilds:
            guild_name = guild.name
            guild_id = guild.id

            if guild.member_count:
                console.info(f"Fetching members from {guild_name}")

                try:
                    await guild.fetch_members(force_scraping=True, cache=True)

                except discord.ClientException:
                    console.warning(
                        f"ClientException: fetch_members() failed fo {guild_name}"
                    )
                    try:
                        channel_target = discord.Object(
                            guild.text_channels[0].id, type=Snowflake
                        )
                        await guild.fetch_members(
                            force_scraping=True,
                            cache=True,
                            channels=channel_target,  # ty:ignore[invalid-argument-type]
                        )

                    except discord.InvalidData:
                        console.warning(
                            f"InvalidData: Failed to fetch {guild_name} due to InvalidData"
                        )

                    except Exception as err:
                        console.warning(
                            f"{str(err)} while processing {guild_name} (id: {guild_id})"
                        )

                except BaseException as err:
                    console.info(
                        f"{str(err)} while processing {guild_name} (id: {guild_id})"
                    )

            self.df = pd.concat([self.df, self.print_members_formatted(self, guild_id)])

        self.df.to_csv(self.csv_path, index=False)

        exit()

    def print_members_formatted(self, client: discord.Client, guild_id):
        guild = client.get_guild(guild_id)
        tmp_df = pd.DataFrame()

        if guild is not None:
            members = guild.members
            console.debug(
                f"▶️▶️▶️   GUILD : {guild.name}  (members count {len(members)} / {guild.member_count})"
            )
            for member in members:
                is_friend = member.is_friend()
                console.debug(
                    f"   {member.name:<30} -  {member.id:<24} - friend ? : {is_friend}"
                )

                data = {
                    "id": [member.id],
                    "name": [member.name],
                    "is_friend": [is_friend],
                    "guild_name": [guild.name],
                    "guild_id": [guild.id],
                }

                # data = {k: [v] for k, v in data.items()}

                tmp_df = pd.concat(
                    [
                        tmp_df,
                        pd.DataFrame(data),
                    ]
                )

        return tmp_df


if __name__ == "__main__":
    client = MyClient()
    client.run(get_token())
