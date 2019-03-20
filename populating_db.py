from faker import Faker
import random
import records

USERNAME = ''
PASSWORD = ''
DB_NAME = ''

PIZZAS = "Buffalo,Calzone,Chicken BBQ,Chicken Cheese,Chorizo,Delicatessen,Hot Fever,Merguez,Régina," \
         "Royale,Spéciale,Végétarienne,Fajitas,Océane,4 Fromages,Chèvre,Raclette,Rustique,Steack," \
         "Tartiflette,La Roquefort,La Munster".split(",")

INGREDIENTS = "Coulis de tomate,Tabasco,Baparella,Oignons,Poivrons,Poulet,Crème fraîche,Guacamole,Mozzarella,Saumon," \
              "Crevettes,Persillade,Citron,Cheddar,Reblochon,Miel,Oeuf,Thon,Moutarde,Tomates,Cornichons," \
              "Lardons".split(",")

STATUTS_COMMANDE = ["En attente", "En préparation", "En cours de livraison", "Terminée"]

PIZZERIAS_OWNER = 'OC Pizza'
NUMBER_OF_TYPE_EMPLOYEES = 5  # Will be equivalent to Livreur - Responsable Commande - Pizzaïolo etc...
NUMBER_OF_PIZZERIAS = 5
NUMBER_OF_INGREDIENTS = 10  # Max 22
NUMBER_OF_PIZZAS = 10  # Max 22
NUMBER_OF_CLIENTS = 20
NUMBER_OF_COMMANDES = 20


fake = Faker('fr_FR')


def clients_creation(number):
    # We are creating an "owner client" before adding the random ones
    fake_clients = [{'nom': PIZZERIAS_OWNER, 'prenom': PIZZERIAS_OWNER, 'mail': 'OCPizza@openclassrooms.com'}]

    for _ in range(1, number):
        fake_clients.append({'nom': fake.last_name(), 'prenom': fake.first_name(), 'mail': fake.email()})

    return fake_clients


def ingredients_creation(number):
    fake_ingredients = []

    # We make sure that every ingredient is UNIQUE
    while len(fake_ingredients) < number:
        ingredient = {'nom': fake.word(ext_word_list=INGREDIENTS)}
        if ingredient not in fake_ingredients:
            fake_ingredients.append(ingredient)
        else:
            pass

    return fake_ingredients


def pizzas_creation(number):
    fake_pizzas = []
    pizzas_copy = PIZZAS.copy()

    # We make sure that every pizza is UNIQUE and not modifying the constant PIZZAS
    for _ in range(0, number):
        pizza = fake.word(ext_word_list=pizzas_copy)
        pizzas_copy.remove(pizza)
        pizza = {'nom': pizza, 'prix': f'{random.uniform(10, 25):.04}'}
        fake_pizzas.append(pizza)

    return fake_pizzas


def type_employe_creation(number):
    fake_type_employes = []

    while len(fake_type_employes) < number:
        job = fake.job().strip()
        type_employe = {'nom_type': job}

        # We make sure that the job is unique and that the name isn't over the limit VARCHAR(50)
        if type_employe not in fake_type_employes and len(job) < 50:
            fake_type_employes.append(type_employe)
        else:
            pass

    return fake_type_employes


def factures_creation(number):
    fake_factures = []

    for _ in range(0, number):
        fake_factures.append({'date': fake.date_this_decade(),
                              'payee': fake.boolean(),
                              'lien': fake.url()})

    return fake_factures


def adresses_creation(db, number):
    fake_adresses = []
    client_ids = _get_table_ids(db, 'client')
    oc_pizza_id = db.query("SELECT * FROM client WHERE nom = :owner", owner=PIZZERIAS_OWNER)
    client_ids.remove(oc_pizza_id.first().id)  # We remove the client OC Pizza as the addresses will be pizzerias

    # We are creating the addresses of the pizzerias that'll be used in the pizzeria table
    for _ in range(0, NUMBER_OF_PIZZERIAS):
        fake_adresses.append({'client_id': oc_pizza_id.first().id,
                              'code_postal': f'{random.randint(1000, 99000):05}',
                              'ville': fake.city(),
                              'rue': fake.street_name(),
                              'numero_habitation': fake.building_number()
                              })

    # Addresses of clients.
    # As many addresses as clients. A client can have several addresses. So some clients don't have any address.
    for _ in range(0, number):
        fake_adresses.append({'client_id': random.choice(client_ids),
                              'code_postal': f'{random.randint(1000, 99000):05}',
                              'ville': fake.city(),
                              'rue': fake.street_name(),
                              'numero_habitation': fake.building_number()
                              })

    return fake_adresses


def recettes_creation(db):
    fake_recettes = []
    pizza_ids = _get_table_ids(db, 'pizza')

    for _ in range(0, len(pizza_ids)):
        rdm_pizza_id = pizza_ids.pop(random.randrange(len(pizza_ids)))
        fake_recettes.append({'recette': fake.text(max_nb_chars=500),
                              'pizza_id': rdm_pizza_id})

    return fake_recettes


def pizzerias_creation(db):
    fake_pizzerias = []

    # Getting the id of OC Pizza
    oc_client_id = db.query("SELECT * FROM client WHERE nom = :owner", owner=PIZZERIAS_OWNER)
    # Getting the addresses linked to the id
    oc_adresses = db.query("SELECT * FROM adresse_livraison WHERE client_id = :oc_id",
                           oc_id=oc_client_id.first().id)

    oc_adresse_ids = [row.id for row in oc_adresses]

    # Generating pizzerias based on the addresses we created specifically in adresses_creation()
    for _ in range(0, NUMBER_OF_PIZZERIAS):
        adresse_id = oc_adresse_ids.pop(random.randrange(len(oc_adresse_ids)))
        fake_pizzerias.append({'nom': fake.sentence(nb_words=2),
                               'adresse_id': adresse_id})

    return fake_pizzerias


def employe_creation(db):
    fake_employes = []
    type_employe_ids = _get_table_ids(db, 'type_employe')

    # Generating between 5/10 employees for each pizzeria
    for pizzeria_id in range(1, NUMBER_OF_PIZZERIAS + 1):
        for _ in range(0, random.randint(5, 11)):
            fake_employes.append({'nom': fake.last_name(),
                                  'prenom': fake.first_name(),
                                  'pizzeria_id': pizzeria_id,
                                  'type_employe_id': random.choice(type_employe_ids)
                                  })

    return fake_employes


def compte_employe_creation(db):
    fake_accounts = []
    employe_ids = _get_table_ids(db, 'employe')

    for id in employe_ids:
        fake_accounts.append({'employe_id': id,
                              'username': fake.user_name(),
                              'password': fake.password()
                              })

    return fake_accounts


def stock_creation(db):
    fake_stocks = []
    pizzeria_ids = _get_table_ids(db, 'pizzeria')
    ingredient_ids = _get_table_ids(db, 'ingredient')

    for pizzeria_id in pizzeria_ids:
        for ingredient_id in ingredient_ids:
            fake_stocks.append({'pizzeria_id': pizzeria_id,
                                'ingredient_id': ingredient_id,
                                'quantite': f'{random.uniform(0, 999):.6}'  # Between 0/999kg in stock
                                })

    return fake_stocks


def composition_creation(db):
    fake_compositions = []
    pizza_ids = _get_table_ids(db, 'pizza')
    ingredient_ids = _get_table_ids(db, 'ingredient')

    for pizza_id in pizza_ids:
        # There'll be between 2-7 ingredients in each pizza
        rdm_ingredients_ids = set(random.choices(ingredient_ids, k=random.randint(2, 7)))
        for ingredient_id in rdm_ingredients_ids:
            fake_compositions.append({'pizza_id': pizza_id,
                                      'ingredient_id': ingredient_id,
                                      'quantite': f'{random.uniform(0, 0.5):.2}'  # Between 0/0.5kg per ingredient
                                      })

    return fake_compositions


def statut_creation():
    fake_statut = []

    for statut in STATUTS_COMMANDE:
        fake_statut.append({'statut': statut})

    return fake_statut


def commande_creation(db, number):
    fake_commandes = []
    oc_pizza_id = db.query("SELECT * FROM client WHERE nom = :owner", owner=PIZZERIAS_OWNER)
    client_ids = _get_table_ids(db, 'client')
    client_ids.remove(oc_pizza_id.first().id)
    pizzeria_ids = _get_table_ids(db, 'pizzeria')
    statut_ids = _get_table_ids(db, 'statut_commande')

    for _ in range(0, number):
        pizzeria_id = random.choice(pizzeria_ids)
        # We get the employees working in the pizzeria_id
        employe_ids_query = db.query("SELECT id FROM employe WHERE pizzeria_id = :pizzeria_id",
                                     pizzeria_id=pizzeria_id)
        employe_ids = [row.id for row in employe_ids_query]

        adresse_ids = []
        while not adresse_ids:  # In case the client doesn't have any address
            client_id = random.choice(client_ids)
            adresse_ids = db.query("SELECT id from adresse_livraison WHERE client_id = :client_id",
                                   client_id=client_id)
            adresse_ids = [row.id for row in adresse_ids]  # Empty if no address corresponding to the client

        fake_commandes.append({'client_id': client_id,
                               'adresse_livraison_id': random.choice(adresse_ids),
                               'pizzeria_id': pizzeria_id,
                               'responsable_id': random.choice(employe_ids),
                               'statut_id': random.choice(statut_ids)
                               })

    return fake_commandes


def panier_creation(db, number):
    fake_paniers = []
    pizza_ids = _get_table_ids(db, 'pizza')
    commande_ids = _get_table_ids(db, 'commande', pk="numero")

    for _ in range(0, number):
        commande_id = commande_ids.pop(random.randrange(len(commande_ids)))
        pizza_ids_copy = pizza_ids.copy()  # To respect the UNIQUE constraint of one pizza type per command
        for _ in range(0, random.randint(0, 3)):  # Between one and three paniers (aka pizza type) per command
            pizza = pizza_ids_copy.pop(random.randrange(len(pizza_ids_copy)))
            quantite = random.randint(1, 10)
            prix = _get_total_sum(db, pizza, quantite)

            fake_paniers.append({'type_pizza': pizza,
                                 'numero_commande': commande_id,
                                 'quantite': quantite,
                                 'prix': prix})

    return fake_paniers


def livraison_creation(db):
    fake_livraisons = []
    commandes_ids = _get_table_ids(db, 'commande', pk="numero")
    factures_ids = _get_table_ids(db, 'facture', pk="numero")
    livreur_ids = _get_table_ids(db, 'employe')

    for _ in range(0, NUMBER_OF_COMMANDES):
        rdm_commande = commandes_ids.pop(random.randrange(len(commandes_ids)))
        rdm_facture = factures_ids.pop(random.randrange(len(factures_ids)))

        fake_livraisons.append({'date': fake.date_this_decade(),
                                'commande_numero': rdm_commande,
                                'facture_numero': rdm_facture,
                                'livreur_id': random.choice(livreur_ids)
                                })

    return fake_livraisons


def _get_total_sum(db, pizza, quantity):
    price_query = db.query("SELECT prix from pizza WHERE id = :pizza", pizza=pizza)
    price = price_query.first().prix
    price = price * quantity

    return round(price, 2)


def _get_table_ids(db, table, pk="id"):
    rows = db.query(f'SELECT * from {table}')
    if pk == "id":
        ids = [row.id for row in rows]
    elif pk == "numero":  # For commande/facture table
        ids = [row.numero for row in rows]
    else:
        print(f"The column {pk} does not exists")
        return []

    return ids


def main():
    db = records.Database(f'postgres://{USERNAME}:{PASSWORD}@localhost/{DB_NAME}')

    fake_clients = clients_creation(NUMBER_OF_CLIENTS)
    db.bulk_query('INSERT INTO client (nom, prenom, mail) VALUES (:nom, :prenom, :mail)', fake_clients)

    fake_ingredients = ingredients_creation(NUMBER_OF_INGREDIENTS)
    db.bulk_query('INSERT INTO ingredient (nom) VALUES (:nom)', fake_ingredients)

    fake_pizzas = pizzas_creation(NUMBER_OF_PIZZAS)
    db.bulk_query('INSERT INTO pizza (nom, prix) VALUES (:nom, :prix)', fake_pizzas)

    fake_type_employe = type_employe_creation(NUMBER_OF_TYPE_EMPLOYEES)
    db.bulk_query('INSERT INTO type_employe (nom_type) VALUES (:nom_type)', fake_type_employe)

    fake_factures = factures_creation(NUMBER_OF_COMMANDES)
    db.bulk_query('INSERT INTO facture (date, payee, lien) VALUES (:date, :payee, :lien)', fake_factures)

    fake_adresses = adresses_creation(db, NUMBER_OF_CLIENTS)
    db.bulk_query('INSERT INTO adresse_livraison (client_id, code_postal, ville, rue, numero_habitation)'
                  'VALUES (:client_id, :code_postal, :ville, :rue, :numero_habitation)', fake_adresses)

    fake_recettes = recettes_creation(db)
    db.bulk_query('INSERT INTO recette (recette, pizza_id) VALUES (:recette, :pizza_id)', fake_recettes)

    fake_pizzerias = pizzerias_creation(db)
    db.bulk_query('INSERT INTO pizzeria (nom, adresse_id) VALUES (:nom, :adresse_id)', fake_pizzerias)

    fake_employes = employe_creation(db)
    db.bulk_query('INSERT INTO employe (nom, prenom, pizzeria_id, type_employe_id) '
                  'VALUES (:nom, :prenom, :pizzeria_id, :type_employe_id)', fake_employes)

    fake_compte_employes = compte_employe_creation(db)
    db.bulk_query('INSERT INTO compte_employe (employe_id, username, password)'
                  'VALUES (:employe_id, :username, :password)', fake_compte_employes)

    fake_stocks = stock_creation(db)
    db.bulk_query('INSERT INTO stock (pizzeria_id, ingredient_id, quantite)'
                  'VALUES (:pizzeria_id, :ingredient_id, :quantite)', fake_stocks)

    fake_compositions = composition_creation(db)
    db.bulk_query('INSERT INTO composition (pizza_id, ingredient_id, quantite)'
                  'VALUES (:pizza_id, :ingredient_id, :quantite)', fake_compositions)

    fake_statuts = statut_creation()
    db.bulk_query('INSERT INTO statut_commande (statut) VALUES (:statut)', fake_statuts)

    fake_commandes = commande_creation(db, NUMBER_OF_COMMANDES)
    db.bulk_query('INSERT INTO commande (client_id, adresse_livraison_id, pizzeria_id, responsable_id, statut_id)'
                  'VALUES (:client_id, :adresse_livraison_id, :pizzeria_id, '
                  ':responsable_id, :statut_id)', fake_commandes)

    fake_paniers = panier_creation(db, NUMBER_OF_COMMANDES)
    db.bulk_query('INSERT INTO panier (type_pizza, numero_commande, quantite, prix)'
                  'VALUES (:type_pizza, :numero_commande, :quantite, :prix)', fake_paniers)

    fake_livraisons = livraison_creation(db)
    db.bulk_query('INSERT INTO livraison (date, commande_numero, facture_numero, livreur_id)'
                  'VALUES (:date, :commande_numero, :facture_numero, :livreur_id)', fake_livraisons)


if __name__ == '__main__':
    # Wipe your DB if you want to populate it again ! README.md
    main()
