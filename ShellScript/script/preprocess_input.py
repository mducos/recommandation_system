import pandas as pd
import json
import difflib
from colorama import Fore, Style

def verify_input(input_file):
    # Initialize lists to store genres and formats
    genres = []
    formats = []

    # Read the input CSV file into a DataFrame
    input_file_df = pd.read_csv(input_file)

    # Load the author2title2book mapping from the JSON file
    with open('data/author2title2book.json') as file:
        author2title = json.load(file)

    # Iterate over each row in the DataFrame
    for index, row in input_file_df.iterrows():
        author = row['Auteur']  # Extract the author name
        title = row['Titre']    # Extract the book title

        # Check if the author is in the database
        if author not in author2title:
            print(Fore.RED + "\n/!\\ Author not found in the database: " + author + Style.RESET_ALL)

            # Find the three most similar authors using difflib
            similar_authors = difflib.get_close_matches(author, author2title.keys(), n=3)

            if len(similar_authors) > 0:
                # Print the three most similar authors
                print(f"The closest authors to \"{author}\" are:")
                for i in range(len(similar_authors)):
                    print(f"|{i+1}| {similar_authors[i]}")

                # Ask the user if they want to modify the author with one of the suggested authors
                user_choice = ""
                while user_choice not in ["1", "2", "3", "n"]:
                    user_choice = input("-----> Which suggestion do you want to use to modify the author? [1|2|3|n] ")
                    if user_choice == "1" and len(similar_authors) > 0:
                        author = similar_authors[0]  # Modify the author with the first suggestion
                    elif user_choice == "2" and len(similar_authors) > 1:
                        author = similar_authors[1]  # Modify the author with the second suggestion
                    elif user_choice == "3" and len(similar_authors) > 2:
                        author = similar_authors[2]  # Modify the author with the third suggestion
                    elif user_choice == "n":
                        author2title[author] = {}
                        author2title[author][title] = [{"Synopsis (str)": "", "Genre (List(str))": "", "Format (str)": ""}]
                    else:
                        user_choice = ""

                if user_choice != "n":
                    # Update the author in the DataFrame and save the modified DataFrame to the CSV file
                    input_file_df.at[index, 'Auteur'] = author
                    input_file_df.to_csv(input_file, index=False)
                    print(Fore.GREEN + "The author has been successfully modified." + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + "The author has been added to the database." + Style.RESET_ALL)

        # Check if the title is in the list of books for the author
        if title not in author2title[author]:
            print(Fore.RED + "\n/!\\ Title not found among the books of " + author + ": " + title + Style.RESET_ALL)

            # Find the three most similar titles using difflib
            similar_title = difflib.get_close_matches(title, author2title[author].keys(), n=3)

            if len(similar_title) > 0:
                # Print the three most similar titles
                print(f"The closest titles to \"{title}\" are:")
                for i in range(len(similar_title)):
                    print(f"|{i+1}| {similar_title[i]}")

                # Ask the user if they want to modify the title with one of the suggested titles
                user_choice = ""
                while user_choice not in ["1", "2", "3", "n"]:
                    user_choice = input("-----> Which suggestion do you want to use to modify the title? [1|2|3|n] ")
                    if user_choice == "1" and len(similar_title) > 0:
                        title = similar_title[0]  # Modify the title with the first suggestion
                    elif user_choice == "2" and len(similar_title) > 1:
                        title = similar_title[1]  # Modify the title with the second suggestion
                    elif user_choice == "3" and len(similar_title) > 2:
                        title = similar_title[2]  # Modify the title with the third suggestion
                    elif user_choice == "n":
                        author2title[author][title] = {"Synopsis (str)": "", "Genre (List(str))": "", "Format (str)": ""}
                    else:
                        user_choice = ""

                if user_choice != "n":
                    # Update the title in the DataFrame and save the modified DataFrame to the CSV file
                    input_file_df.at[index, 'Titre'] = title
                    input_file_df.to_csv(input_file, index=False)
                    print(Fore.GREEN + "The title has been successfully modified." + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + "The title has been added to the database." + Style.RESET_ALL)

        # If the author is in the database, check if the title is also present
        if author in author2title:
            if title in author2title[author]:
                # Append the genre and format of the book to the respective lists
                genres.append(author2title[author][title][0]['Genre (List(str))'])
                formats.append(author2title[author][title][0]['Format (str)'])

    # Print a success message after verifying all the books
    print(Fore.GREEN + "\nAll books have been successfully verified.\n" + Style.RESET_ALL)

    # Return the unique genres and formats as sets
    return set(genres), set(formats)
