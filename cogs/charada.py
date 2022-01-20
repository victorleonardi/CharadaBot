from tracemalloc import stop
from turtle import title
import discord
import asyncio
from random import randint
from discord.ext import commands
from difflib import SequenceMatcher


class Charada(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.list_of_all_riddles = [
            ('eco', 'Eu falo sem boca e ouço sem ouvidos. Não tenho corpo, mas com o ar me torno vivo.'),
            ('vela', 'Você mede minha vida em horas e eu o sirvo expirando. Sou rápido quando fino e lento quando grosso. O vento é meu inimigo'),
            ('mapa', 'Eu tenho cidades, mas não casa. Eu tenho montanhas, mas não árvores. Eu tenho água, mas nenhum peixe.'),
            ('r', 'O que é visto no meio de Março e Abril e não pode ser visto no inicio ou fim de ambos os meses?'),
            ('selo', 'Sem sair do meu espaço, sou capaz de viajar por todo o mundo.'),
            ('gelo', 'Dela sou feito, porém, se nela me encontrar, em questão de tempo eu desapareço.'),
            ('papel', 'Aguento qualquer queda sem problemas. Contudo, no mais subito respingo, me ruino.'),
            ('respiração', 'Sou sutil e leve como uma pena. Contudo, nem mesmo o mais musculoso é capaz de me segurar por mais de um minuto.')
        ]
        self.list_of_riddles_used_in_the_month = []
        self.answer_riddle = ""
        self.user_winner = None
        self.chances_for_answer_role = 3
        self.chances_for_answer_riddle = 3

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')

    # Commands
    @commands.guild_only()
    @commands.command()
    async def charada(self, ctx):
        n = randint(0, (len(self.list_of_all_riddles) - 1))
        self.answer_riddle, text_riddle = self.list_of_all_riddles[n]
        self.list_of_riddles_used_in_the_month.append(
            self.list_of_all_riddles[n])
        self.list_of_all_riddles.remove(self.list_of_all_riddles[n])
        await ctx.send(text_riddle)

    @commands.guild_only()
    @commands.command()
    async def resp(self, ctx, resposta: str):
        resposta = resposta.lower()
        print(self.answer_riddle)
        try:
            if resposta in self.answer_riddle:
                self.user_winner = ctx.author
                await ctx.send("Certo... Infeliz")
                embed = discord.Embed(
                    title="Cargos", description="Cargos que você pode escolher para ser promovido para \n" + '\n'.join([str(role.name) for role in ctx.guild.roles]))
                await ctx.send(embed=embed)
            if resposta not in self.answer_riddle:
                self.chances_for_answer_riddle -= 1
                await ctx.send(f"Infelizmente, você errou... Você só tem mais {self.chances_for_answer_riddle} chances para acertar.")
        except:
            await ctx.send('Parece que você esqueceu alguma coisa para falar comigo, verme. Tente novamente')

    @commands.guild_only()
    @commands.command()
    async def prize(self, ctx, cargo: str):
        if ctx.author == self.user_winner:
            if self.chances_for_answer_role > 0:
                try:
                    for role in ctx.guild.roles:
                        proxy_role = SequenceMatcher(
                            None, cargo.lower(), str(role).lower()).ratio()
                        if proxy_role > 0.5:
                            estimate_role = str(role)
                            break
                    give_role = discord.utils.get(
                        ctx.guild.roles, name=estimate_role)
                    user = ctx.author
                    await user.add_roles(give_role)
                    await ctx.send("Feito, miserával.")
                except:
                    self.chances_for_answer_role -= 1
                    await ctx.send(f"Otário, você tem mais {self.chances_for_answer_role} chances.")
            else:
                self.user_winner = None
                self.chances_for_answer_role = 3
                await ctx.send("Você perdeu todas suas chances, palhaço.")

    @commands.command()
    async def Teste(self, ctx):
        print(ctx.guild.roles)
        for role in ctx.guild.roles:
            print(role, type(role))


def setup(client):
    client.add_cog(Charada(client))
