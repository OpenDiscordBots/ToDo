from json import dumps
from random import choice

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog, Param, slash_command

from src.bot import Bot


class Todo(Cog):
    """Core commands for ToDo"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self._todos = {}

    @slash_command(name="todo")
    async def todo(
        self,
        ctx: ApplicationCommandInteraction,
        task: str = Param(desc="The task you need to do"),
    ) -> None:
        """Create a new todo task."""

        if not (todos := self._todos.get(f"{ctx.author.id}")):
            todos = (await self.bot.api.kv_get(f"{ctx.author.id}")) or []

        todos.append(task)

        await self.bot.api.kv_set(f"{ctx.author.id}", dumps(todos))
        self._todos[f"{ctx.author.id}"] = todos

        await ctx.send(f"Successfully created your new todo task!", ephemeral=True)

    @slash_command(name="todos")
    async def todos(self, ctx: ApplicationCommandInteraction) -> None:
        """List all todo tasks."""

        if not (todos := self._todos.get(f"{ctx.author.id}")):
            todos = (await self.bot.api.kv_get(f"{ctx.author.id}")) or []

        message = ""

        for i, todo in enumerate(todos):
            message += f"{i + 1}: {todo}\n"

        await ctx.send(message or "No todos to display!", ephemeral=True)

    @slash_command(name="done")
    async def done(
        self,
        ctx: ApplicationCommandInteraction,
        task: int = Param(desc="The task you have completed"),
    ) -> None:
        """Mark a todo task as completed."""

        if not (todos := self._todos.get(f"{ctx.author.id}")):
            todos = (await self.bot.api.kv_get(f"{ctx.author.id}")) or []

        if task <= 0 or task > len(todos):
            await ctx.send(f"Invalid task number.", ephemeral=True)
            return

        todos.pop(task - 1)

        await self.bot.api.kv_set(f"{ctx.author.id}", dumps(todos))
        self._todos[f"{ctx.author.id}"] = todos

        await ctx.send(f"Successfully marked your todo task as completed!", ephemeral=True)

    @slash_command(name="pick")
    async def pick(
        self,
        ctx: ApplicationCommandInteraction,
    ) -> None:
        """Pick a todo task at random."""

        if not (todos := self._todos.get(f"{ctx.author.id}")):
            todos = (await self.bot.api.kv_get(f"{ctx.author.id}")) or []

        if not todos:
            await ctx.send(f"No todos to pick from!", ephemeral=True)
            return

        todo = choice(todos)

        await ctx.send(f"Here's a random task you need to do:\n\n{todo}", ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(Todo(bot))
