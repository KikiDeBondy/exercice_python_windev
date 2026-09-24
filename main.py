## Utilisage de Claude Code pour : 
## - Avoir la bonne syntaxe python, car je ne connais pas très bien ce langage
## - Factoriser le calcul du rabais par lot : structurer le calcul en triant 
##   les prix unitaires de la catégorie pour identifier les articles les 
##   moins chers de chaque tranche de 3

## Reflexion par moi même, sans IA : 
## - Ajouter une fonction qui calculera le taux de remise, il faut réaliser une foncion générique, pour pas dupliquer le code
## - L'ordre des remises et des rabais doit être correct pour obtenir le total final exact
## - Ne pas oublier l'arrondi du total final


#La fonction ci-dessous permet de récup le taux de remise en fonction de la quantité d'articles
def get_volume_discount(qty: int, volume_discounts: dict) -> float:
    discount = 0.0
    for seuil, rate in sorted(volume_discounts.items(), reverse=True):
        if qty >= seuil:
            discount = rate
            break
    return discount


def calculate_total(cart: list[dict], rules: dict) -> float:
    # Pour chaque article dans notre panier, on applique la remise s'il est nécessaire
    for item in cart:
        # On récupère ici via la fonction, le taux de remise (en fonction du nombre d'articles)
        discount = get_volume_discount(item["qty"], rules["volume_discounts"])
        # On applique la remise sur le prix unitaire de l'article
        item["unit_price_discounted"] = item["price"] * (1 - discount)

    # Calcul du total après application des remises unitaires
    total = sum(item["unit_price_discounted"] * item["qty"] for item in cart)

    # Calcul du rabais pour les lots par catégorie éligible
    for category in rules["bundle_categories"]:
        # liste à plat de tous les prix unitaires remisés pour cette catégorie
        prices = []
        for item in cart:
            if item["category"] == category:
                # On ajoute le prix unitaire remisé de cet article autant de fois que sa quantité
                prices.extend([item["unit_price_discounted"]] * item["qty"])

        # du moins cher au plus cher
        prices.sort()
        # nombre d'articles gratuits (1 par tranche de 3)
        nb_free = len(prices) // 3 

        # les nb_free moins chers sont gratuits donc on les soustrait du total
        total -= sum(prices[:nb_free])

    return round(total, 2)



## Données de test
rules = {
    "volume_discounts": {5: 0.10, 10: 0.20}, # qty >= 5: -10%, qty >= 10: -20%
    "bundle_categories": ["book"] # 3e offert par tranche de 3
}

cart = [
    {"id": "A", "category": "book", "price": 10.0, "qty": 4},
    {"id": "B", "category": "book", "price": 15.0, "qty": 1},
    {"id": "C", "category": "tech", "price": 100.0, "qty": 1},
]

result = calculate_total(cart, rules)
print("Résultat obtenu :", result)
assert result == 145