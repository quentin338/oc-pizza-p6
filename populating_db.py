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

fake = Faker('fr_FR')


def clients_creation(number):
    fake_clients = []

    for _ in range(0, number):
        fake_clients.append({'nom': fake.last_name(), 'prenom': fake.first_name(), 'mail': fake.email()})

    return fake_clients


def ingredients_creation(number):
    fake_ingredients = []

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

    for _ in range(0, number):
        pizza = fake.word(ext_word_list=pizzas_copy)
        pizzas_copy.remove(pizza)
        pizza = {'nom': pizza, 'prix': f'{random.uniform(10, 25):.04}'}
        fake_pizzas.append(pizza)

    return fake_pizzas


def type_employe_creation(number):
    fake_type_employes = []
    unique_job = []

    while len(fake_type_employes) < number:
        job = fake.job().strip()
        if job not in unique_job and len(job) < 50:
            unique_job.append(job)
            fake_type_employes.append({'nom_type': job})
        else:
            pass

    return fake_type_employes


def factures_creation(number):
    fake_factures = []

    for _ in range(0, number):
        rdm_bool = random.choice(('True', 'False'))
        fake_factures.append({'date': fake.date_this_decade(),
                              'payee': rdm_bool,
                              'lien': fake.url()})

    return fake_factures


def adresses_creation(db, number):
    fake_adresses = []
    client_ids = _get_table_ids(db, 'client')

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
        rdm_pizza_id = random.choice(pizza_ids)
        pizza_ids.remove(rdm_pizza_id)
        fake_recettes.append({'recette': fake.text(max_nb_chars=500),
                              'pizza_id': rdm_pizza_id})

    return fake_recettes


def _get_table_ids(db, table):
    ids = []
    rows = db.query(f'SELECT * from {table}')

    for row in rows:
        ids.append(row['id'])

    return ids


def main():
    db = records.Database(f'postgres://{USERNAME}:{PASSWORD}@localhost/{DB_NAME}')

    # fake_clients = clients_creation(10)
    # db.bulk_query('INSERT INTO client (nom, prenom, mail) VALUES (:nom, :prenom, :mail)', fake_clients)

    # fake_ingredients = ingredients_creation(10)
    # db.bulk_query('INSERT INTO ingredient (nom) VALUES (:nom)', fake_ingredients)

    # fake_pizzas = pizzas_creation(10)
    # db.bulk_query('INSERT INTO pizza (nom, prix) VALUES (:nom, :prix)', fake_pizzas)

    # fake_type_employe = type_employe_creation(10)
    # db.bulk_query('INSERT INTO type_employe (nom_type) VALUES (:nom_type)', fake_type_employe)

    # fake_factures = factures_creation(10)
    # db.bulk_query('INSERT INTO facture (date, payee, lien) VALUES (:date, :payee, :lien)', fake_factures)

    # fake_adresses = adresses_creation(db, 10)
    # db.bulk_query('INSERT INTO adresse_livraison (client_id, code_postal, ville, rue, numero_habitation)'
    #               'VALUES (:client_id, :code_postal, :ville, :rue, :numero_habitation)', fake_adresses)

    # fake_recettes = recettes_creation(db)
    # db.bulk_query('INSERT INTO recette (recette, pizza_id) VALUES (:recette, :pizza_id)', fake_recettes)


if __name__ == '__main__':
    main()
