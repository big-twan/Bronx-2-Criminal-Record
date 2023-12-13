import discord
from discord.ext import commands
import aiohttp
from aiohttp import request
from datetime import datetime
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request
from charges import charges_sort, charges_format, time_to_timestamp
import time
import dateutil.parser
  

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='b!', intents=intents)

time_pos = [(140, 735), (140, 820),(140, 905),(140, 990),(140, 1075)]
charges_pos = [(320, 735), (320, 820),(320, 905),(320, 990),(320, 1075)]
sentences_pos = [(500, 735), (500, 820),(500, 905),(500, 990),(500, 1075)]
statuses_pos = [(670, 735), (670, 820),(670, 905),(670, 990),(670, 1075)]

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def record(ctx, name):
    checked = False
    mainUrl = f"https://users.roblox.com/v1/usernames/users"
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=mainUrl, json={"usernames":[name],"excludeBannedUsers": True})
        data = await response.json()

        if data["data"] == []:
            await ctx.send(":x: User was not found in the database.")

        else:
            id = data['data'][0]['id']
            real_name = data['data'][0]['name']
            checked = True  
    
    if not checked:
        return

    
    avatarUrl = f"https://thumbnails.roblox.com/v1/users/avatar-bust?userIds={id}&size=150x150&format=Png&isCircular=false"

    async with request("GET", avatarUrl) as response:
        if response.status == 200:
            data = await response.json()
            avatar = data['data'][0]['imageUrl']

        # await ctx.send(avatar)

        prison = "https://media.istockphoto.com/id/506499561/photo/white-grunge-brick-wall-background.jpg?s=612x612&w=0&k=20&c=SJVmtzPWObNCz4wTUywaXZFC_g2w7x0FxFOiabaj20c="

        urllib.request.urlretrieve(prison, "prison.png") 
        urllib.request.urlretrieve(avatar, "avatar.png") 


        box = (0,0,170,170)
        pilImg1 = Image.open("prison.png")
        pilImg1 = pilImg1.crop(box)
        copy1 = pilImg1.copy()
        pilImg2 = Image.open("avatar.png")
        # print(pilImg2.size)
        copy2 = pilImg2.copy()


        copy1.paste(copy2, (10, 20), copy2.convert('RGBA'))

        template = Image.open("NYPD Template.png")
        template_2d = ImageDraw.Draw(template)
        font = ImageFont.truetype("fonts/gudea/Gudea-Bold.ttf", 40)
        template_2d.text((408, 425), f"{id} - {real_name}", fill="black", anchor="ms", font=font)
        template_2d.text((408,482), "birthday", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

        copy1 = copy1.resize((275,275))
        template.paste(copy1, (273, 94), copy1.convert('RGBA'))

        clean = template.copy()
        use = template.copy()
        template_2d = ImageDraw.Draw(use)


        priors = charges_sort(real_name)[0]
        times = charges_sort(real_name)[1]
        charges = charges_sort(real_name)[2]
        sentences = charges_sort(real_name)[3]
        og_name = charges_sort(real_name)[4]

        # if og_name != real_name:
        #     await ctx.send(":white_check_mark: This player has no criminal history!")
        #     return

        # print(times)

        
        for i in range(len(times)):
            total_charges = len(times)
            if total_charges <= 4:
                pages = 1
            else:
                if total_charges % 4 == 0:
                    pages = total_charges // 4
                else:
                    pages = (total_charges // 4) + 1

            #pages += 1
            #print(times)

            if i == 4:
                break
            template_2d.text(time_pos[i], (times[i]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
            template_2d.text(charges_pos[i], (charges_format(", ".join(charges[i]))), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 22))
            template_2d.text(sentences_pos[i], (sentences[i][:-4]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))


            if i == 0:
                stamp_setup = dateutil.parser.parse(time_to_timestamp(times[0]))
                first_time = stamp_setup.timestamp()
                diff = (time.time()) - first_time
                # print(diff)

                if diff >= int(sentences[0].split(" ")[0]):
                    template_2d.text(statuses_pos[i], "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

                    locked = False
                    template_2d.text((408,517), "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

                else:
                    template_2d.text(statuses_pos[i], "In Custody", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                    locked = True
                    template_2d.text((408,517), "In Custody", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
            
            else:
                template_2d.text(statuses_pos[i], "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

            # diff = time.time() - time_to_timestamp(times[i])
            # print(diff)

            

        # print(template.size)
    

        # with io.BytesIO() as image_binary:
        #     copy1.save(image_binary, 'PNG')
        #     image_binary.seek(0)
        #     await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

        page = 1

        with io.BytesIO() as image_binary2:
            use.save(image_binary2, 'PNG')
            image_binary2.seek(0)
            msg = await ctx.send(file=discord.File(fp=image_binary2, filename='Criminal Record.png'))

        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        reactions = ["⬅️","➡️"]

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions
        
        
        while True:


            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                # print(pages)
                await msg.remove_reaction(str(reaction.emoji),user)

                clean = template.copy()
                template_2d_n = ImageDraw.Draw(clean)
                if str(reaction.emoji) == "➡️":
                    # await msg.remove_attachments(msg.attachments)
                    if page < pages:
                        page += 1


                    if locked:
                        template_2d_n.text((408,517), "In Custody", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                    else:
                        template_2d_n.text((408,517), "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                    # print(f"page{page} pages{pages}")
                    if page != pages:
                        for i in range(4):
                            template_2d_n.text(time_pos[i], (times[i+(4*(page-1))]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                            template_2d_n.text(charges_pos[i], (charges_format(", ".join(charges[i+(4*(page-1))]))), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 22))
                            template_2d_n.text(sentences_pos[i], (sentences[i+(4*(page-1))][:-4]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                            template_2d_n.text(statuses_pos[i], "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                    else:
                        # template_2d_n.text((408,517), "In Custody", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28)) if locked else template_2d.text((408,517), "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

                        for i in range(total_charges - (4*(page-1))):
                            template_2d_n.text(time_pos[i], (times[i+(4*(page-1))]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                            template_2d_n.text(charges_pos[i], (charges_format(", ".join(charges[i+(4*(page-1))]))), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 22))
                            template_2d_n.text(sentences_pos[i], (sentences[i+(4*(page-1))][:-4]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                            template_2d_n.text(statuses_pos[i], "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

                    with io.BytesIO() as image_binary2_n:
                        clean.save(image_binary2_n, 'PNG')
                        image_binary2_n.seek(0)
                        await msg.edit(attachments=[discord.File(fp=image_binary2_n, filename='Criminal Record.png')])

                elif str(reaction.emoji) == "⬅️":

                    if page - 1 >= 1:
                        page -= 1

                        if locked:
                            template_2d_n.text((408,517), "In Custody", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                        else:
                            template_2d_n.text((408,517), "Released", fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))

                        for i in range(4):
                            template_2d_n.text(time_pos[i], (times[i+(4*(page-1))]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                            template_2d_n.text(charges_pos[i], (charges_format(", ".join(charges[i+(4*(page-1))]))), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 22))
                            template_2d_n.text(sentences_pos[i], (sentences[i+(4*(page-1))][:-4]), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))
                            template_2d_n.text(statuses_pos[i], ("Released" if (page-1) == 0 else "In Custody" if locked else "Released"), fill="black", anchor="ms", font=ImageFont.truetype("fonts/gudea/Gudea-Regular.ttf", 28))


                    
                        with io.BytesIO() as image_binary2_n:
                            clean.save(image_binary2_n, 'PNG')
                            image_binary2_n.seek(0)
                            await msg.edit(attachments=[discord.File(fp=image_binary2_n, filename='Criminal Record.png')])



    

        # with io.BytesIO() as image_binary2_n:
        #     clean.save(image_binary2_n, 'PNG')
        #     image_binary2_n.seek(0)
        #     await msg.edit(attachments=[discord.File(fp=image_binary2_n, filename='Criminal Record.png')])




            # try:
            #     reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            # except asyncio.TimeoutError:  #<---- If the user doesn't respond
            #     pass
            # else:
            #     await ctx.send('e')
            # await msg.add_files('avatar.png')
    #         avatar = data["data"][0]["state"]
    #         if avatar == "Blocked":
    #             embed = discord.Embed(title=f"{username}'s Roblox Stats", description=f'Roblox stats for **{username}**', color=0x000001)
    #             embed.add_field(name="General", value=f"`- Username:` {username}\n`- Nickname:` {nickname}\n`- ID:` {rblxId}\n`- Status:` \"{status}\"\n`- Is Banned:` {str(isBanned).title()}\n`- Created At:` {createdAtDef}")
    #             embed.timestamp = datetime.utcnow()
    #             embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)

    #             await ctx.send(embed=embed)
    #         else:
    #             embed = discord.Embed(title=f"{username}'s Roblox Stats", description=f'Roblox stats for **{username}**', color=0x000001)
    #             embed.add_field(name="General", value=f"`- Username:` {username}\n`- Nickname:` {nickname}\n`- ID:` {rblxId}\n`- Status:` \"{status}\"\n`- Is Banned:` {str(isBanned).title()}\n`- Created At:` {createdAtDef}")
    #             embed.set_thumbnail(url=f"{avatarPic.get('imageUrl')}")
    #             embed.timestamp = datetime.utcnow()
    #             embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)

    #             await ctx.send(embed=embed)



bot.run('MTE3NjA0Mjg4MTczMjA2MzM0Mg.G47Lyp.R-0mtIyQtnghQWXpvH8qASyYs6IckUUMNDaYF8')