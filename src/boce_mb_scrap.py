import json
from urllib.request import urlopen

def fetch_and_save_html(url, output_file):
    """
    Fetches HTML content from a URL and saves it to a file.
    """
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"HTML content fetched and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while fetching HTML: {e}")

def process_aadiparv(input_file, output_file):
    """
    Reads text from the input file starting from line 13, removes blank lines,
    splits the 'text' field into 'number' and 'text' fields, and further splits the 'number'
    field into 'book', 'chapter', 'verse', and 'quarter_verse'. Saves the final JSON.
    """
    try:
        # Open the input file and read lines
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Remove blank lines
        lines = [line for line in lines if line.strip()]

        # Start processing from line 13 (index 12)
        verses = []
        for i, line in enumerate(lines[6:], start=7):  # Start numbering from line 13
            line = line.strip()
            if line:  # Skip empty lines (already filtered, but double-check)
                # Split the line into number and text
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    number = parts[0]
                    text = parts[1]

                    # Split the number field into book, chapter, verse, and quarter_verse
                    book = number[:2]
                    chapter = number[2:5]
                    verse = number[5:8]
                    quarter_verse = number[8:]

                    verses.append({
                        "line_number": i - 6,
                        "book": book,
                        "chapter": chapter,
                        "verse": verse,
                        "quarter_verse": quarter_verse,
                        "text": text
                    })
                else:
                    number = parts[0]
                    verses.append({
                        "line_number": i - 6,
                        "book": number[:2],
                        "chapter": number[2:5],
                        "verse": number[5:8],
                        "quarter_verse": number[8:],
                        "text": ""
                    })

        # Write the final JSON output to a file
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(verses, json_file, ensure_ascii=False, indent=4)

        print(f"Successfully processed and saved final JSON to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def club_verses(input_file, output_file):
    """
    Combines JSON elements with the same verse, removes line_number and quarter_verse,
    and adds book and chapter fields. The text is combined with a newline character.
    """
    # Load the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Dictionary to store combined verses
    combined_verses = {}

    # Iterate through the JSON elements
    for item in data:
        book = item['book']  # Extract the book number
        chapter = item['chapter']  # Extract the chapter number
        verse = item['verse']  # Extract the verse number
        text = item['text']  # Extract the text

        # Create a unique key for each book, chapter, and verse combination
        key = (book, chapter, verse)

        # Combine text for the same verse
        if key in combined_verses:
            combined_verses[key] += ' \n ' + text
        else:
            combined_verses[key] = text

    # Prepare the output JSON structure
    output_data = [
        {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "text": text
        }
        for (book, chapter, verse), text in combined_verses.items()
    ]

    # Write the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Combined verses saved to {output_file}")


def main():
    """
    Main function to orchestrate the fetching and processing of the Mahabharata text.
    """
    url = "https://bombay.indology.info/mahabharata/text/UD/MBh01.txt"
    html_file = "../data/html/aadiparv.html"
    json_file = "../data/json/aadiparv.json"
    json_file_for_speech = "../data/json/aadiparv_sarvam.json"

    # Step 1: Fetch and save the HTML content
    fetch_and_save_html(url, html_file)

    # Step 2: Convert the HTML content to JSON
    process_aadiparv(html_file,json_file)

    #Step 3: Modify json content
    club_verses(json_file,json_file_for_speech)

    
if __name__ == "__main__":
    main()