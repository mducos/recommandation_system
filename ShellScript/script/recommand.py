import argparse
import preprocess_input
import process

# Create an argument parser object
parser = argparse.ArgumentParser()

# Add the --book_liked_path argument
parser.add_argument("--book_liked_path", required=True, help="Books liked by the user. CSV format.")
# Add the --author_out argument with a default value of False
parser.add_argument("--author_out", required=False, default=False, action='store_true', help="Recommend authors in the list of liked books. Boolean.")

# Parse the arguments from the command line
args = parser.parse_args()
input_file = args.book_liked_path  # Get the path to the input file
author_out = args.author_out       # Get the value of the author_out flag

# Verify the input file and get the genres and formats
genres, formats = preprocess_input.verify_input(input_file)

# Get the top 10 book recommendations based on the input file, authors to remove, genres, and formats
process.get_top_10_titles(input_file, author_out, genres, formats)