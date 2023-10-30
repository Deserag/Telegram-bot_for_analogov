import requests

def search_games():
    url = "https://store.steampowered.com/api/featured/"
    response = requests.get(url)
    data = response.json()

    if data.get('status') != 1:
        print("Ошибка при получении данных.")
        return

    games = data.get('featured_items', [])
    if len(games) == 0:
        print("Ничего не найдено.")
        return

    for game in games[:100]:
        app_id = game.get('id')
        name = game.get('name')
        description = game.get('description')
        genres = game.get('genres')
        price = game.get('price_overview', {}).get('final_formatted')
        store_url = f"https://store.steampowered.com/app/{app_id}"

        print(f"Название: {name}")
        print(f"Описание: {description}")
        print(f"Жанры: {genres}")
        print(f"Цена: {price}")
        print(f"Ссылка: {store_url}")
        print()

# Пример использования
search_games()
