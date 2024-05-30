# Book Recommendation System

## Introduction

This is a book recommendation system that recommends books (only in French) to users based on their liked books.

## Prerequisites

You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Download the database

Download the three files in the `ShellScript/data` folder:
- [`author2title2book.json`](https://drive.google.com/file/d/1aii0jIF04xocE5WUGjibGO4D-YE5Ywo7/view?usp=sharing)
- [`book_database.csv`](https://drive.google.com/file/d/1VX7HHA2yuYeLq_HWHm7BuJwcjHI4BjGa/view?usp=sharing)
- [`format2genre2book.json`](https://drive.google.com/file/d/1iyNnbxL0vX5pw7lag-yIT_yYDmXCoYGq/view?usp=sharing)

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

When you enter the books you like by hand, they may not be written in the same way as in the database, in which case the system will interactively suggest that you modify the title and author to match the data.

If an author is not found, you will find this message:
`/!\ Author not found in the database: [author]`
then, at most three authors from the database will be proposed to you:
```
The closest authors to [author] are:
|1| [suggested author 1]
|2| [suggested author 2]
|3| [suggested author 3]
-----> Which suggestion do you want to use to modify the author? [1|2|3] 
```
you can choose between the three authors, and the modification will be taken into account:
`The author has been successfully modified.`

If a title is not found, you will receive this message:
```
`/!\ Title not found among the books of [author]: [title]`
then, at most three titles from the books of the author in the database will be proposed to you:
The closest titles to \"{title}\" are:
|1| [suggested title 1]
|2| [suggested title 2]
|3| [suggested title 3]
-----> Which suggestion do you want to use to modify the title? [1|2|3] 
```
you can choose between the three titles, and the modification will be taken into account:
`The title has been successfully modified.`

When everything has been reviewed, this message appears:
`All books have been successfully verified.`

#### Second step

Run the script in a shell, and ten book recommandations will appear!
```
Here are the books recommended for you:

author   |        title
author   |        title
author   |        title
author   |        title
author   |        title
author   |        title
author   |        title
author   |        title
author   |        title
author   |        title
```

## Example

Content of `data/books_liked.csv`:

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