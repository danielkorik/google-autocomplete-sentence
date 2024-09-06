import os
import zipfile
import tempfile
from operator import itemgetter
from sentences_trie import SentencesTrie
import shutil

DATA_PATH = "Archive.zip"


class DataManager:
    """
    Manages storage and retrieval of sentences from a ZIP archive and interfaces with a trie for efficient sentence searching.
    """

    def __init__(self):
        """
        Initializes storage structures and sets up a directory for extracting ZIP archives.
        """
        self.sentences_array = []  # List to hold sentence data including the text and its source file info.
        self.sentences_trie = None  # Trie structure for efficient prefix-based sentence retrieval.
        self.temp_dir = None  # Temporary directory for extracting ZIP file contents.
    def extract_archive(self):
        """
        Extracts contents of a specified ZIP archive to a temporary directory.
        Raises FileNotFoundError if the ZIP archive cannot be found.
        """
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"ZIP file '{DATA_PATH}' not found.")
        self.temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(DATA_PATH, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)  # Decompress all files to the temporary directory.

    def populate_sentences(self):
        """
        Populates a list with sentences extracted from text files within the temporary directory.
        Processes only '.txt' files, extracting sentences and their metadata.
        """
        if not self.temp_dir:
            self.extract_zip()  # Extracts the zip if not already extracted.
        for root, _, files in os.walk(self.temp_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, encoding='utf8') as text_file:
                        for line_number, line in enumerate(text_file.readlines(), start=1):
                            self.sentences_array.append({"txt": line.strip(), "file": file[:-4], "line": line_number})
        self.sentences_array.sort(key=itemgetter('txt'))  # Sorts the sentences lexicographically.

    def initialize_trie(self):
        """
        Initializes the trie with sentences for efficient search operations, indexing each sentence and its suffixes.
        """
        self.sentences_trie = SentencesTrie()
        for index, sentence in enumerate(self.sentences_array):
            for start_pos in range(len(sentence['txt'])):
                self.sentences_trie.insert_sentence(sentence['txt'][start_pos:], (index, start_pos))
    def initialize_data(self):
        """
        Performs a comprehensive initialization or reset of data structures by loading text files and populating the trie.
        """
        print("Loading the files...")
        self.extract_archive()
        self.populate_sentences()
        self.initialize_trie()
        print("The system is ready :)")

    def fetch_sentence_data(self, index):
        """
        Fetches sentence data including the text and its metadata based on its index in the sentences list.

        Args:
            index (int): Index of the sentence in the list.

        Returns:
            tuple: Sentence text and its file location and line number.
        """
        sentence = self.sentences_array[index]
        return sentence['txt'], f"{sentence['file']}, Line: {sentence['line']}"

    def get_trie_structure(self):
        """
        Provides access to the trie structure for external querying.

        Returns:
            SentencesTrie: The trie object for sentence querying.
        """
        return self.sentences_trie

    def __del__(self):
        """
        Cleans up by deleting the temporary directory when the DataManager instance is destroyed.
        """
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
