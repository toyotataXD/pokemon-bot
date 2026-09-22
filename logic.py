import aiohttp
import random


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        if pokemon_trainer not in Pokemon.pokemons:
            self.pokemon_trainer = pokemon_trainer
            self.pokemon_number = random.randint(1, 1000)
            self.name = None
            self.img_url = None
            self.hp = None
            self.power = None
            Pokemon.pokemons[pokemon_trainer] = self

    async def get_data(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    raw_name = data["name"]
                    self.name = raw_name.split("-")[0].capitalize()
                    self.img_url = data["sprites"]["front_default"]

                    stats = {
                        stat["stat"]["name"]: stat["base_stat"]
                        for stat in data["stats"]
                    }
                    self.hp = stats.get("hp", random.randint(50, 100))
                    self.power = stats.get("attack", random.randint(30, 90))
                else:
                    self.name = "Pikachu"
                    self.img_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
                    self.hp = 35
                    self.power = 55

    async def get_name(self):
        if not self.name:
            await self.get_data()
        return self.name

    async def info(self):
        if not self.name:
            await self.get_data()
        return f"İsim: {self.name}, Can: {self.hp}, Güç: {self.power}"

    async def show_img(self):
        if not self.img_url:
            await self.get_data()
        return self.img_url

    async def attack(self, enemy):
        if not self.name:
            await self.get_data()
        if not enemy.name:
            await enemy.get_data()

        if isinstance(enemy, Wizard):
            sans = random.randint(1, 5)
            if sans == 1:
                return f"{enemy.name} kalkan kullandi ve hasar almadi!"

        enemy.hp -= self.power

        if enemy.hp <= 0:
            enemy.hp = 0
            return f"{self.name}, {enemy.name} pokemonuna {self.power} hasar vurdu! Kazanan: {self.pokemon_trainer}!"
        else:
            return f"{self.name}, {enemy.name} pokemonuna {self.power} hasar vurdu! {enemy.name} kalan can: {enemy.hp}"


class Wizard(Pokemon):
    async def attack(self, enemy):
        return await super().attack(enemy)


class Fighter(Pokemon):
    async def attack(self, enemy):
        sans = random.randint(1, 100)
        if sans <= 30:
            super_guc = random.randint(5, 15)
            self.power += super_guc
            sonuc = await super().attack(enemy)
            self.power -= super_guc
            return sonuc + f"\nDövüşçü Pokémon süper saldırı kulland! Eklenen güç: {super_guc}"
        else:
            return await super().attack(enemy)