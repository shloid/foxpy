# lastfm.py
# Last.fm plugin for Fox

from discord.ext import commands
import config
import json
import requests
import datetime
from box import Box
from discord.ext import commands
import discord


class LastFm:

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.api_key = config.LFM_API_KEY
        self.base_user_url = "http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={0}&api_key={1}&format=json"
        self.base_track_url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={0}&api_key={1}" \
                              "&format=json"

    @commands.command()
    async def profile(self):
        u = self.base_user_url.format(self.user, self.api_key)
        u2 = self.base_track_url.format(self.user, self.api_key)
        p = requests.get(u)
        p2 = requests.get(u2)
        # Error codes for user details: http://www.last.fm/api/show/user.getInfo
        # Error codes for user's recent tracks: http://www.last.fm/api/show/user.getRecentTracks
        await self.bot.say("Getting users profile details... please wait.")
        if config.DEBUG:
            await self.bot.say("**lfm**: p status code was `{0}`".format(p.status_code))
            await self.bot.say("**lfm**: p2 status code was `{0}`".format(p2.status_code))
            await self.bot.say("**lfm**: p encoding is `{0}`".format(p.encoding))
            await self.bot.say("**lfm**: p2 encoding is `{0}`".format(p2.encoding))
            await self.bot.say("**lfm**: parsing json to box")
        else:
            u_details = json.loads(p.content)
            u_playing = json.loads(p2.content)

            # Convert json dict to Box
            ud = Box(u_details)
            up = Box(u_playing)

            if config.DEBUG:
                await self.bot.say("**lfm**: done!")
            else:
                embed = discord.Embed(title="Last.fm Profile", colour=discord.Colour(0x7c998c),
                                      url=ud.user.url, timestamp=datetime.datetime.utcnow())

                embed.set_author(name=ud.user.name, url=ud.user.url,
                                 icon_url=ud.user.image)
                embed.set_footer(text="Generated by Fox", icon_url=self.bot.user.default_avatar_url)
                # if up.recenttracks.track[0]:
                #     embed.add_field(name="**Currently Scrobbling**", value=up.recenttracks.track[0])
                # else:
                #     embed.add_field(name="**Currently Scrobbling**", value="Not scrobbling anything")
                # embed.add_field(name="__Last Scrobbled Tracks__",
                #                value="1. asdf\n2. asdasd\n3. asfdsfsd\n4. sdfsf\n5. dsfdsfds")
                try:
                    await self.bot.say(content="Here's the details for that Last.fm user:", embed=embed)
                except discord.HTTPException as e:
                    await self.bot.say("Sorry, I encountered an error doing that. `{0}`".format(e))


def setup(bot):
    bot.add_cog(LastFm(bot))
