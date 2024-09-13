# utils.py

import random

def generate_player_name():
    first_names = ['Ace', 'King', 'Queen']
    last_names = ['OfSpades', 'OfHearts', 'OfDiamonds', 'OfClubs']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def format_currency(amount):
    """Форматируем сумму в денежный формат."""
    return "${:,.2f}".format(amount)
