import csv
from wordcloud import WordCloud, STOPWORDS

def read_csv_and_generate_wordcloud(csv_file, output_image):
    """Read the content column from a CSV file and generate a word cloud."""
    try:
        custom_stopwords = set(STOPWORDS)
        custom_stopwords.update(["movie", "film", "movies", "films", "character", "characters"])

        # Read the 'Content' column from the CSV file
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            all_text = " ".join(row['Content'] for row in reader if 'Content' in row)

        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=400, background_color="white",
                              stopwords=custom_stopwords).generate(all_text)

        # Save the word cloud to an image file
        wordcloud.to_file(output_image)
        print(f"Word cloud saved to {output_image}")

    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except KeyError:
        print("Error: The CSV file does not have a 'Content' column.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    print("Word Cloud Generator from CSV\n")
    csv_file = input("Enter the path to the CSV file: ")
    output_image = input("Enter the output image file name (e.g., wordcloud.png): ")
    read_csv_and_generate_wordcloud(csv_file, output_image)
