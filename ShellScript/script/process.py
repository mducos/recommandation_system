import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stop_words import get_stop_words
import json

def get_reference_content(input_file_path):
    """
    Extracts the synopsis content from the books listed in the input CSV file
    to create a reference content string.

    Parameters:
    input_file_path (str): Path to the input CSV file containing author and title columns.

    Returns:
    str: A concatenated string of synopses from the books listed in the input file.
    """
    reference_content = ""
    
    # Read the input CSV file into a DataFrame
    with open(input_file_path, 'r') as input_file:
        input_file_df = pd.read_csv(input_file)
        
        # Load the author to book mapping from the JSON file
        with open('data/author2title2book.json', 'r') as db_file:
            author2book = json.load(db_file)

        # Iterate over each row in the DataFrame
        for index, row in input_file_df.iterrows():
            author = row['Auteur']  # Extract the author name
            title = row['Titre']    # Extract the book title
            
            # Check if the author and title are in the database
            if author in author2book and title in author2book[author]:
                synopsis = author2book[author][title][0]['Synopsis (str)']
                reference_content += synopsis + " "  # Concatenate the synopsis to the reference content

    return reference_content

def get_authors_to_remove(input_file_path):
    """
    Extracts the list of authors from the input CSV file whose books should be removed
    from the recommendation pool.

    Parameters:
    input_file_path (str): Path to the input CSV file containing author and title columns.

    Returns:
    list: A list of authors to remove.
    """
    authors_to_remove = []
    
    # Read the input CSV file into a DataFrame
    with open(input_file_path, 'r') as input_file:
        input_file_df = pd.read_csv(input_file)
        
        # Iterate over each row in the DataFrame
        for index, row in input_file_df.iterrows():
            author = row['Auteur']  # Extract the author name
            authors_to_remove.append(author)  # Append the author to the list

    return authors_to_remove

def get_top_10_titles(input_file_path, authors_to_remove, genres, formats):
    """
    Recommends the top 10 book titles based on the content similarity of the synopses
    in the reference content.

    Parameters:
    input_file_path (str): Path to the input CSV file containing author and title columns.
    authors_to_remove (list): List of authors to exclude from recommendations.
    genres (set): Set of genres to include in recommendations.
    formats (set): Set of formats to include in recommendations.

    Returns:
    None
    """
    # Get the reference content from the input file
    reference_content = get_reference_content(input_file_path)

    # Get the French stop words
    stop_words = get_stop_words('fr')

    # Load the format to genre to book mapping from the JSON file
    with open('data/format2genre2book.json', 'r') as format2genre2book_file:
        format2genre2book = json.load(format2genre2book_file)

    # Initialize an empty DataFrame to store books
    df_books = pd.DataFrame()

    # Iterate over the formats and genres to populate the DataFrame
    for format in formats:
        for genre in genres:
            if format in format2genre2book and genre in format2genre2book[format]:
                books = format2genre2book[format][genre]
                if df_books.empty:
                    df_books = pd.DataFrame(books)
                else:
                    df_books = pd.concat([df_books, pd.DataFrame(books)])

    # Replace NaN values with empty strings
    df_books.fillna(" ", inplace=True)

    # Read the input CSV file into a DataFrame
    with open(input_file_path, 'r') as input_file:
        input_file_df = pd.read_csv(input_file)

    # Remove books that are already in the input file
    df_books = df_books[~df_books['Titre (str)'].isin(input_file_df['Titre'])]

    df_books['Saga Title'] = df_books['Titre (str)'].str.split(", tome ").str[0]
    df_books['Tome Number'] = df_books['Titre (str)'].str.split(", tome ").str[1].str.split(" : ").str[0].str.extract('(\d+)').astype(float)

    # Replace NaN values with empty strings
    df_books.fillna(0, inplace=True)

    # Remove books with a tome number lower than the maximum tome number
    for title, author in zip(input_file_df['Titre'], input_file_df['Auteur']):
        if ", tome " in title:
            saga_title = title.split(", tome ")[0]
            tome_number = title.split(", tome ")[1].split(" : ")[0]
            
            df_books = df_books[~((df_books['Auteur (str)'] == author) & 
                                  (df_books['Saga Title'] == saga_title) & 
                                  ((df_books['Tome Number'] < float(tome_number)) | 
                                   (df_books['Tome Number'] > float(int(tome_number) + 1))))]
            
    # Extract the synopses for TFIDF vectorization
    documents = df_books['Synopsis (str)']

    # Initialize the TFIDF vectorizer with French stop words
    vectoriseur_tfidf = TfidfVectorizer(stop_words=stop_words)

    # If there are authors to remove, filter them out from the DataFrame
    if authors_to_remove:
        authors_to_remove = get_authors_to_remove(input_file_path)
        df_books.reset_index(drop=True, inplace=True)
        mask = ~(df_books['Auteur (str)'].isin(authors_to_remove))
        mask = mask.reindex(df_books.index)
        documents = df_books.loc[mask]
        matrice_tfidf = vectoriseur_tfidf.fit_transform(documents['Synopsis (str)'])
    else:
        matrice_tfidf = vectoriseur_tfidf.fit_transform(documents)

    # Calculate cosine similarity between the reference content and the TFIDF matrix
    similarite_documents = cosine_similarity(vectoriseur_tfidf.transform([reference_content]), matrice_tfidf)[0]

    # Convert the similarity scores to a Series with document indices
    similarite_series = pd.Series(similarite_documents, index=documents.index)

    # Get the top 10 similar documents
    top_10_similarities = similarite_series.nlargest(10)

    print("Here are the books recommended for you:\n")
    max_author_length = 0
    for doc_id in top_10_similarities.index:
        max_author_length = max(max_author_length, len(df_books.loc[doc_id, 'Auteur (str)']))
    # Print the recommended books
    for doc_id in top_10_similarities.index:
        author = df_books.loc[doc_id, 'Auteur (str)']
        title = df_books.loc[doc_id, 'Titre (str)']
        print(f"{author.ljust(max_author_length)} \t| {title}")
    print()