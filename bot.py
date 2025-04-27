import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Slash-Commands synchronisiert: {len(synced)}')
    except Exception as e:
        print(f'Fehler beim Synchronisieren der Slash-Commands: {e}')

@bot.tree.command(name="einstellen", description="Stellt ein neues Teammitglied ein")
@app_commands.describe(mitglied="Das Mitglied, das eingestellt wird", rolle="Die Rolle, die zugewiesen wird")
async def einstellen(interaction: discord.Interaction, mitglied: discord.Member, rolle: discord.Role):
    if interaction.guild.me.top_role <= rolle:
        await interaction.response.send_message("❌ Ich kann diese Rolle nicht zuweisen, da sie höher oder gleich meiner höchsten Rolle ist.", ephemeral=True)
        return

    try:
        await mitglied.add_roles(rolle)
        embed = discord.Embed(
            title="✅ Einstellung erfolgreich",
            description=f"{mitglied.mention} wurde als {rolle.mention} eingestellt.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Eingestellt von {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Ich habe nicht die Berechtigung, diese Rolle zuzuweisen.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ein Fehler ist aufgetreten: {e}", ephemeral=True)

@bot.tree.command(name="entlassen", description="Entlässt ein Teammitglied")
@app_commands.describe(mitglied="Das Mitglied, das entlassen wird", rolle="Die Rolle, die entfernt wird")
async def entlassen(interaction: discord.Interaction, mitglied: discord.Member, rolle: discord.Role):
    if interaction.guild.me.top_role <= rolle:
        await interaction.response.send_message("❌ Ich kann diese Rolle nicht entfernen, da sie höher oder gleich meiner höchsten Rolle ist.", ephemeral=True)
        return

    try:
        await mitglied.remove_roles(rolle)
        embed = discord.Embed(
            title="🛑 Entlassung erfolgreich",
            description=f"{mitglied.mention} wurde von der Rolle {rolle.mention} entlassen.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Entlassen von {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Ich habe nicht die Berechtigung, diese Rolle zu entfernen.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ein Fehler ist aufgetreten: {e}", ephemeral=True)

@bot.tree.command(name="rolle", description="Weist einem Mitglied eine Rolle zu")
@app_commands.describe(mitglied="Das Mitglied, dem die Rolle zugewiesen wird", rolle="Die Rolle, die zugewiesen wird")
async def rolle(interaction: discord.Interaction, mitglied: discord.Member, rolle: discord.Role):
    if interaction.guild.me.top_role <= rolle:
        await interaction.response.send_message("❌ Ich kann diese Rolle nicht zuweisen, da sie höher oder gleich meiner höchsten Rolle ist.", ephemeral=True)
        return

    try:
        await mitglied.add_roles(rolle)
        embed = discord.Embed(
            title="🔧 Rolle zugewiesen",
            description=f"{rolle.mention} wurde erfolgreich an {mitglied.mention} vergeben.",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Zugewiesen von {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Ich habe nicht die Berechtigung, diese Rolle zuzuweisen.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ein Fehler ist aufgetreten: {e}", ephemeral=True)

@bot.tree.command(name="info", description="Zeigt Informationen über ein Mitglied an")
@app_commands.describe(mitglied="Das Mitglied, über das Informationen angezeigt werden")
async def info(interaction: discord.Interaction, mitglied: discord.Member):
    roles = [role.mention for role in mitglied.roles if role != interaction.guild.default_role]
    embed = discord.Embed(
        title=f"ℹ️ Informationen über {mitglied}",
        color=discord.Color.purple()
    )
    embed.add_field(name="Benutzername", value=mitglied.name, inline=True)
    embed.add_field(name="ID", value=mitglied.id, inline=True)
    embed.add_field(name="Beigetreten am", value=mitglied.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Rollen", value=", ".join(roles) if roles else "Keine Rollen", inline=False)
    embed.set_thumbnail(url=mitglied.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="befördern", description="Befördert ein Mitglied zu einer höheren Rolle")
@app_commands.describe(mitglied="Das Mitglied, das befördert wird", alte_rolle="Die zu entfernende Rolle", neue_rolle="Die neue Rolle, die zugewiesen wird")
async def befoerdern(interaction: discord.Interaction, mitglied: discord.Member, alte_rolle: discord.Role, neue_rolle: discord.Role):
    if interaction.guild.me.top_role <= alte_rolle or interaction.guild.me.top_role <= neue_rolle:
        await interaction.response.send_message("❌ Ich kann diese Rollen nicht ändern, da sie höher oder gleich meiner höchsten Rolle sind.", ephemeral=True)
        return

    try:
        await mitglied.remove_roles(alte_rolle)
        await mitglied.add_roles(neue_rolle)
        embed = discord.Embed(
            title="📈 Beförderung erfolgreich",
            description=f"{mitglied.mention} wurde von {alte_rolle.mention} entfernt und erhielt {neue_rolle.mention}.",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Befördert von {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Ich habe nicht die Berechtigung, diese Rollen zu ändern.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ein Fehler ist aufgetreten: {e}", ephemeral=True)

@bot.tree.command(name="derank", description="Degradiert ein Mitglied zu einer niedrigeren Rolle")
@app_commands.describe(mitglied="Das Mitglied, das degradiert wird", alte_rolle="Die zu entfernende Rolle", neue_rolle="Die neue Rolle, die zugewiesen wird")
async def derank(interaction: discord.Interaction, mitglied: discord.Member, alte_rolle: discord.Role, neue_rolle: discord.Role):
    if interaction.guild.me.top_role <= alte_rolle or interaction.guild.me.top_role <= neue_rolle:
        await interaction.response.send_message("❌ Ich kann diese Rollen nicht ändern, da sie höher oder gleich meiner höchsten Rolle sind.", ephemeral=True)
        return

    try:
        await mitglied.remove_roles(alte_rolle)
        await mitglied.add_roles(neue_rolle)
        embed = discord.Embed(
            title="📉 Degradierung erfolgreich",
            description=f"{mitglied.mention} wurde von {alte_rolle.mention} entfernt und erhielt {neue_rolle.mention}.",
            color=discord.Color.dark_gray()
        )
        embed.set_footer(text=f"Degradiert von {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Ich habe nicht die Berechtigung, diese Rollen zu ändern.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ein Fehler ist aufgetreten: {e}", ephemeral=True)


# BOT starten
bot.run('MTM2NDY1NDg0NzAyMTgwOTY3NA.G2RdaW.64rHe73qJhz5Iuj-nh23YOCNLGDIC_m_Fw9o74')

