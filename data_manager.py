import os
import zipfile
from operator import itemgetter
from sentences_trie import SentencesTrie
import tempfile

DATA_PATH = "Archive.zip"


class DataManager:

    def __init__(self):
        self.sentences_array = []
        self.sentences_trie = None
        self.temp_dir = None

    def extract_zip(self):
        """Extract ZIP file to a temporary directory"""
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"ZIP file '{DATA_PATH}' not found.")

        self.temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        with zipfile.ZipFile(DATA_PATH, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)  # Extract all files to the temp directory

    def reboot_array(self):
        """Read the files and insert sentences with data to the array of sentences"""
        if not self.temp_dir:
            self.extract_zip()  # Ensure ZIP is extracted

        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.endswith('.txt'):  # Make sure only text files are read
                    file_path = os.path.join(root, file)
                   # print(f"Loading file: {file}")  # Print the name of the file being loaded
                    with open(file_path, encoding='utf8') as text_file:
                        line_number = 0
                        for line in text_file.readlines():
                            line_number += 1
                            self.sentences_array.append(
                                {"txt": line.strip(), "file": file.replace(".txt", ""), "line": line_number})

        # Sort sentences array by the text
        self.sentences_array = sorted(self.sentences_array, key=itemgetter('txt'))

    def reboot_trie(self):
        """Insert each sentence with all its suffixes to the trie of suffixes"""
        self.sentences_trie = SentencesTrie()
        for i in range(len(self.sentences_array)):
            for j in range(len(self.sentences_array[i]['txt'])):
                self.sentences_trie.insert_sentence(self.sentences_array[i]['txt'][j:], (i, j))

    def reboot(self):
        """Reboot the system with all the needed data"""
        print("Loading the files and preparing the system...")
        self.extract_zip()  # Extract ZIP content
        self.reboot_array()  # Load sentences into array
        self.reboot_trie()  # Insert sentences into trie
        print("The system is ready :)")

    def get_sentence_data(self, sentence_index):
        """Get an index and return the data of the sentence in this index in the array"""
        return self.sentences_array[sentence_index][
                   'txt'], f"{self.sentences_array[sentence_index]['file']}, {self.sentences_array[sentence_index]['line']}"

    def get_trie(self):
        """Return the trie pointer"""
        return self.sentences_trie

    def __del__(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)