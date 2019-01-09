import argparse
import bs4
import genanki
import random
import requests

def create_deck():
    # Modify first string to create hierarchical deck
    DECK_HIERARCHY = 'A2'+'::'

    # Parse vocab url, ex: https://learngerman.dw.com/en/bei-uns-oder-bei-euch/l-38209600/lv
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', nargs='*')
    args = parser.parse_args()

    URL = str(args.URL[0])
    print(URL)

    # Create random deck ID for Anki
    UNIQ_DECK_ID = random.randrange(1 << 30, 1 << 31)

    # Parse URL and get list of vocab words
    res = requests.get(URL)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    vocab_list = soup.findAll("div", {"class": "row vocabulary "})
    title = soup.findAll("div", {"class": "excercise-nav-title "})[0]
    title = DECK_HIERARCHY + title.getText().strip('\n')

    my_model = genanki.Model(
        UNIQ_DECK_ID,
        "Nico's Weg Flashcards",
        fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        ],
        templates=[
        {
          'name': 'Card 1',
          'qfmt': '{{Question}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
        ])

    my_deck = genanki.Deck(UNIQ_DECK_ID, title)

    # Parse English and German vocab
    for vocab in vocab_list:
        vocab_de = str(vocab.select('strong')[0].getText())
        vocab_en = str(vocab.select('p')[-1].getText())

        my_note = genanki.Note(
            model=my_model,
            fields=[vocab_de, vocab_en])

        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file(title + '.apkg')
    print(title + ' is complete')

if __name__ == '__main__':
    create_deck()

