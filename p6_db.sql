
CREATE SEQUENCE public.statut_commande_id_seq;

CREATE TABLE public.statut_commande (
                id INTEGER NOT NULL DEFAULT nextval('public.statut_commande_id_seq'),
                statut VARCHAR(40) NOT NULL,
                CONSTRAINT statut_commande_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.statut_commande_id_seq OWNED BY public.statut_commande.id;

CREATE UNIQUE INDEX statut_commande_idx
 ON public.statut_commande
 ( statut );

CREATE SEQUENCE public.type_employe_id_seq;

CREATE TABLE public.type_employe (
                id INTEGER NOT NULL DEFAULT nextval('public.type_employe_id_seq'),
                nom_type VARCHAR(50) NOT NULL,
                CONSTRAINT type_employe_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.type_employe_id_seq OWNED BY public.type_employe.id;

CREATE UNIQUE INDEX type_employe_idx
 ON public.type_employe
 ( nom_type );

CREATE SEQUENCE public.ingredient_id_seq;

CREATE TABLE public.ingredient (
                id INTEGER NOT NULL DEFAULT nextval('public.ingredient_id_seq'),
                nom VARCHAR(80) NOT NULL,
                CONSTRAINT ingredient_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.ingredient_id_seq OWNED BY public.ingredient.id;

CREATE UNIQUE INDEX ingredient_idx
 ON public.ingredient
 ( nom );

CREATE SEQUENCE public.facture_numero_seq;

CREATE TABLE public.facture (
                numero INTEGER NOT NULL DEFAULT nextval('public.facture_numero_seq'),
                date DATE NOT NULL,
                payee BOOLEAN NOT NULL,
                lien VARCHAR(255) NOT NULL,
                CONSTRAINT facture_pk PRIMARY KEY (numero)
);


ALTER SEQUENCE public.facture_numero_seq OWNED BY public.facture.numero;

CREATE SEQUENCE public.client_id_seq;

CREATE TABLE public.client (
                id INTEGER NOT NULL DEFAULT nextval('public.client_id_seq'),
                nom VARCHAR(60) NOT NULL,
                prenom VARCHAR(40) NOT NULL,
                mail VARCHAR(80) NOT NULL,
                CONSTRAINT client_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.client_id_seq OWNED BY public.client.id;

CREATE UNIQUE INDEX client_idx
 ON public.client
 ( nom, prenom, mail );

CREATE SEQUENCE public.adresse_livraison_id_seq;

CREATE TABLE public.adresse_livraison (
                id INTEGER NOT NULL DEFAULT nextval('public.adresse_livraison_id_seq'),
                client_id INTEGER NOT NULL,
                code_postal INTEGER NOT NULL,
                ville VARCHAR(50) NOT NULL,
                rue VARCHAR(100) NOT NULL,
                numero_habitation INTEGER NOT NULL,
                CONSTRAINT adresse_livraison_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.adresse_livraison_id_seq OWNED BY public.adresse_livraison.id;

CREATE SEQUENCE public.pizzeria_id_seq;

CREATE TABLE public.pizzeria (
                id INTEGER NOT NULL DEFAULT nextval('public.pizzeria_id_seq'),
                nom VARCHAR(80) NOT NULL,
                adresse_id INTEGER NOT NULL,
                CONSTRAINT pizzeria_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.pizzeria_id_seq OWNED BY public.pizzeria.id;

CREATE SEQUENCE public.employe_id_seq;

CREATE TABLE public.employe (
                id INTEGER NOT NULL DEFAULT nextval('public.employe_id_seq'),
                nom VARCHAR(60) NOT NULL,
                prenom VARCHAR(40) NOT NULL,
                pizzeria_id INTEGER NOT NULL,
                type_employe_id INTEGER NOT NULL,
                CONSTRAINT employe_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.employe_id_seq OWNED BY public.employe.id;

CREATE TABLE public.compte_employe (
                employe_id INTEGER NOT NULL,
                username VARCHAR(20) NOT NULL,
                password VARCHAR(255) NOT NULL,
                CONSTRAINT compte_employe_pk PRIMARY KEY (employe_id)
);


CREATE TABLE public.stock (
                pizzeria_id INTEGER NOT NULL,
                ingredient_id INTEGER NOT NULL,
                quantite NUMERIC(6,3) NOT NULL,
                CONSTRAINT stock_pk PRIMARY KEY (pizzeria_id, ingredient_id)
);


CREATE UNIQUE INDEX stock_idx
 ON public.stock
 ( pizzeria_id, ingredient_id );

CREATE SEQUENCE public.commande_numero_seq;

CREATE TABLE public.commande (
                numero INTEGER NOT NULL DEFAULT nextval('public.commande_numero_seq'),
                client_id INTEGER NOT NULL,
                adresse_livraison_id INTEGER NOT NULL,
                pizzeria_id INTEGER NOT NULL,
                responsable_id INTEGER NOT NULL,
                statut_id INTEGER NOT NULL,
                CONSTRAINT commande_pk PRIMARY KEY (numero)
);


ALTER SEQUENCE public.commande_numero_seq OWNED BY public.commande.numero;

CREATE SEQUENCE public.livraison_id_seq;

CREATE TABLE public.livraison (
                id INTEGER NOT NULL DEFAULT nextval('public.livraison_id_seq'),
                date DATE NOT NULL,
                commande_numero INTEGER NOT NULL,
                facture_numero INTEGER NOT NULL,
                livreur_id INTEGER NOT NULL,
                CONSTRAINT livraison_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.livraison_id_seq OWNED BY public.livraison.id;

CREATE SEQUENCE public.pizza_id_seq;

CREATE TABLE public.pizza (
                id INTEGER NOT NULL DEFAULT nextval('public.pizza_id_seq'),
                nom VARCHAR(80) NOT NULL,
                prix NUMERIC(4,2) NOT NULL,
                CONSTRAINT pizza_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.pizza_id_seq OWNED BY public.pizza.id;

CREATE UNIQUE INDEX pizza_idx
 ON public.pizza
 ( nom );

CREATE TABLE public.panier (
                type_pizza INTEGER NOT NULL,
                numero_commande INTEGER NOT NULL,
                quantite INTEGER NOT NULL,
                prix NUMERIC(5,2) NOT NULL,
                CONSTRAINT panier_pk PRIMARY KEY (type_pizza, numero_commande)
);


CREATE TABLE public.composition (
                pizza_id INTEGER NOT NULL,
                ingredient_id INTEGER NOT NULL,
                quantite NUMERIC(4,3) NOT NULL,
                CONSTRAINT composition_pk PRIMARY KEY (pizza_id, ingredient_id)
);


CREATE SEQUENCE public.recette_id_seq;

CREATE TABLE public.recette (
                id INTEGER NOT NULL DEFAULT nextval('public.recette_id_seq'),
                recette VARCHAR NOT NULL,
                pizza_id INTEGER NOT NULL,
                CONSTRAINT recette_pk PRIMARY KEY (id)
);


ALTER SEQUENCE public.recette_id_seq OWNED BY public.recette.id;

CREATE UNIQUE INDEX recette_idx
 ON public.recette
 ( pizza_id );

ALTER TABLE public.commande ADD CONSTRAINT statut_commande_commande_fk
FOREIGN KEY (statut_id)
REFERENCES public.statut_commande (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.employe ADD CONSTRAINT type_employe_employe_fk
FOREIGN KEY (type_employe_id)
REFERENCES public.type_employe (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.composition ADD CONSTRAINT ingredient_composition_fk
FOREIGN KEY (ingredient_id)
REFERENCES public.ingredient (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.stock ADD CONSTRAINT ingredient_stock_fk
FOREIGN KEY (ingredient_id)
REFERENCES public.ingredient (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.livraison ADD CONSTRAINT facture_livraison_fk
FOREIGN KEY (facture_numero)
REFERENCES public.facture (numero)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.commande ADD CONSTRAINT client_commande_fk
FOREIGN KEY (client_id)
REFERENCES public.client (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.adresse_livraison ADD CONSTRAINT client_adresse_livraison_fk
FOREIGN KEY (client_id)
REFERENCES public.client (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.commande ADD CONSTRAINT adresse_livraison_commande_fk
FOREIGN KEY (adresse_livraison_id)
REFERENCES public.adresse_livraison (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.pizzeria ADD CONSTRAINT adresse_livraison_pizzeria_fk
FOREIGN KEY (adresse_id)
REFERENCES public.adresse_livraison (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.commande ADD CONSTRAINT pizzeria_commande_fk
FOREIGN KEY (pizzeria_id)
REFERENCES public.pizzeria (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.stock ADD CONSTRAINT pizzeria_stock_fk
FOREIGN KEY (pizzeria_id)
REFERENCES public.pizzeria (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.employe ADD CONSTRAINT pizzeria_employe_fk
FOREIGN KEY (pizzeria_id)
REFERENCES public.pizzeria (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.livraison ADD CONSTRAINT employe_livraison_fk
FOREIGN KEY (livreur_id)
REFERENCES public.employe (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.compte_employe ADD CONSTRAINT employe_compte_employe_fk
FOREIGN KEY (employe_id)
REFERENCES public.employe (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.commande ADD CONSTRAINT employe_commande_fk
FOREIGN KEY (responsable_id)
REFERENCES public.employe (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.panier ADD CONSTRAINT commande_panier_fk
FOREIGN KEY (numero_commande)
REFERENCES public.commande (numero)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.livraison ADD CONSTRAINT commande_livraison_fk
FOREIGN KEY (commande_numero)
REFERENCES public.commande (numero)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.composition ADD CONSTRAINT pizza_composition_fk
FOREIGN KEY (pizza_id)
REFERENCES public.pizza (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.recette ADD CONSTRAINT pizza_recette_fk
FOREIGN KEY (pizza_id)
REFERENCES public.pizza (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.panier ADD CONSTRAINT pizza_panier_fk
FOREIGN KEY (type_pizza)
REFERENCES public.pizza (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
