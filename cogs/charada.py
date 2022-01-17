import discord
import asyncio
from random import randint
from discord.ext import commands


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

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')

    # Commands
    @commands.command()
    async def charada(self, ctx):
        n = randint(0, (len(self.list_of_all_riddles) - 1))
        self.answer_riddle, text_riddle = self.list_of_all_riddles[n]
        self.list_of_riddles_used_in_the_month.append(
            self.list_of_all_riddles[n])
        self.list_of_all_riddles.remove(self.list_of_all_riddles[n])
        await ctx.send(text_riddle)

    @commands.command()
    async def resp(self, ctx, resposta: str):
        resposta = resposta.lower()
        print(self.answer_riddle)
        try:
            if resposta in self.answer_riddle:
                # given_role = discord.utils.get(ctx.guild.roles, name=cargo)
                # await ctx.author.add_roles(given_role)
                await ctx.send("Certo... Infeliz")
            if resposta not in self.answer_riddle:
                await ctx.send('Infelizmente, você errou...')
                await ctx.send('Agora, me diga, qual cargo você deseja como recompensa?')
        except:
            await ctx.send('Parece que você esqueceu alguma coisa para falar comigo, verme. Tente novamente')


def setup(client):
    client.add_cog(Charada(client))
