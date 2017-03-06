# lastfm.py
# Last.fm plugin for Fox

from discord.ext import commands
import config
import json
import requests
import datetime


class LastFm:

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.api_key = config.LFM_API_KEY
        self.base_user_url = "http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={0}&api_key={1}&format=json"
        self.base_track_url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={0}&api_key={1}" \
                              "&format=json"

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
            await self.bot.say("**lfm**: decoding json, please wait...")
        else:
            u_details = p.content
            u_playing = p2.content

            if config.DEBUG:
                await self.bot.say("**lfm**: parsed json successfully.")
            else:
                embed = discord.Embed(title="Last.fm Profile", colour=discord.Colour(0x7c998c),
                                      url=u_details['url'], timestamp=datetime.datetime.utcnow())

                embed.set_author(name=u_details['name'], url=u_details['url'],
                                 icon_url=u_details['image']['size']['small'])
                embed.set_footer(text="Generated by Fox", icon_url=self.bot.user.default_avatar_url)

                embed.add_field(name="**Currently Scrobbling**", value=u_playing['recenttracks']['track'][0])
                # embed.add_field(name="__Last Scrobbled Tracks__",
                #                value="1. asdf\n2. asdasd\n3. asfdsfsd\n4. sdfsf\n5. dsfdsfds")

                await self.bot.say(content="Here's the details for that Last.fm user:", embed=embed)
