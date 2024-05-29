# Book Recommendation System

## Introduction

This is a book recommendation system that recommends books (only in French) to users based on their liked books.

## Prerequisites

You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Command-line Arguments

- `--book_liked_path`: Required. Path to the CSV file containing books liked by the user.
- `--author_out`: Optional. Flag to recommend authors in the list of liked books. If present, authors from user's liked books will not be recommended.

### Running the Script

To run the book recommendation system, use the following command:

```bash
python main.py --book_liked_path=<path_to_csv_file> [--author_out]
```

Replace `<path_to_csv_file>` with the path to your CSV file containing the list of books liked by the user.

#### First step

input process

#### Second step

recommandation

## Example

Content of ```data/books_liked.csv```:

```
Titre,Auteur
"Harry Potter, tome 1 : Harry Potter à l'école des sorciers",J. K. Rowling
"Le Livre des étoiles, tome 2 : Le Seigneur Sha",Erik L'Homme
A comme association tome 1,Erik L'Homme et Pierre Bottero
"Tara Duncan, tome 01 : Les Sortceliers",Sophie Audouin-Mamikonian
"Percy Jackson / Percy Jackson et les Olympiens, tome 1 : Le voleur de foudre",Rick Riordan
"Harry Potter, tome 4 : Harry Potter et la Coupe de feu",J. K. Rowling
```

Command line:

```bash
python main.py --book_liked_path=data/books_liked.csv --author_out
```

This command will recommend books similar to the ones liked by the user and will also recommend authors found in the list of liked books.

Results:
```
Here are the books recommended for you:

David Colbert   |        Les mondes magiques de Harry Potter
Eliezer Yudkowsky       |        Harry Potter et les méthodes de la rationalité
Thomas C. Durand        |        Les énigmes de l'Aube, tome 2 : Les Quatre Vérités
Robert Holdstock        |        La forêt des mythagos, tome 2 : Lavondyss
Carina Rozenfeld        |        L'héritier des Draconis, tome 3 : La baie aux arcs-en-ciel
Thomas Mariani et Sophie Audouin-Mamikonian     |        Les AutresMondes de Tara Duncan, tome 1 : La danse de la licorne
Carrie Bebris   |        Suspense and Sensibility
Jordanna Max Brodsky    |        Olympus Bound, book 1: The Immortals
Raymond E. Feist        |        Les nouvelles chroniques de Krondor / L'entre-deux-guerres / Les Fils de Krondor, tome 2 : Le Boucanier du Roi
Aude Vidal-Lessard      |        Polux, tome 5 : L’éveil du loup
```

## Releases

May 2024: first version of the book recommendation system using TF-IDF and cosine similarity

## What's next?

Some ideas for future improvements and contributions: 
- adapt the recommendation system for films
- create a visual interface with the Django framework
- improve the recommendation algorithm

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.