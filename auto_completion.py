from data_manager import DataManager
import string

RESULT_LEN = 5


class AutoCompletion:
    """
    Handles generating sentence completion suggestions by performing character modifications
    on input sentences and searching a trie structure for matches.
    """

    def __init__(self):
        """
        Initializes the AutoCompletion system with a DataManager instance and defines the score decrement
        for different types of character modifications.
        """
        self.data_manager = DataManager()
        # Scores decrement by edit type to prioritize closer matches.
        self.decrement_scores = {
            "search_replaced": [5, 4, 3, 2, 1],
            "search_added": [10, 8, 6, 4, 2],
            "search_removed": [10, 8, 6, 4, 2]
        }

    def find_replacements(self, sentence, node, idx, num_of_sentences):
        """
        Generates suggestions by replacing each character in the sentence at the specified index and
        searching for these modified sentences in the trie.
        """
        completions = {}
        for letter in string.ascii_lowercase:
            if len(completions) >= num_of_sentences:
                break
            modified_sentence = sentence[:idx] + letter + sentence[idx + 1:]
            result, node = self.data_manager.sentences_trie.search_sentence(modified_sentence, node)
            if result:
                completions.update(result)
        return completions, node

    def find_additions(self, sentence, node, idx, num_of_sentences):
        """
        Generates suggestions by adding each letter of the alphabet at the specified index in the sentence
        and searching for these modified sentences in the trie.
        """
        completions = {}
        for letter in string.ascii_lowercase:
            if len(completions) >= num_of_sentences:
                break
            modified_sentence = sentence[:idx] + letter + sentence[idx:]
            result, node = self.data_manager.sentences_trie.search_sentence(modified_sentence, node)
            if result:
                completions.update(result)
        return completions, node

    def find_removals(self, sentence, node, idx):
        """
        Generates suggestions by removing the character at the specified index from the sentence
        and searching for this modified sentence in the trie.
        """
        modified_sentence = sentence[:idx] + sentence[idx + 1:]
        result, node = self.data_manager.sentences_trie.search_sentence(modified_sentence, node)
        return (result, node) if result else ({}, node)

    def aggregate_completions(self, sentence, node, all_sentence_len):
        """
        Aggregates all potential completions by applying three types of edits:
        replacement, addition, and removal of characters in the sentence.
        Returns up to RESULT_LEN suggestions.
        """
        completions, completions_sentences = [], []
        sentence = sentence.lower().replace("  ", " ")
        base_scores = 2 * all_sentence_len

        result, current_node = self.data_manager.sentences_trie.search_sentence(sentence, node)
        if result:
            completions += self.format_result(result, completions_sentences, base_scores)
            if len(completions) >= RESULT_LEN:
                return completions[:RESULT_LEN], current_node

        # Iterate over each type of character modification
        for idx in reversed(range(len(sentence) + 1)):
            if idx < len(self.decrement_scores["search_replaced"]):
                results = [
                    self.find_replacements(sentence, node, idx, RESULT_LEN - len(completions)),
                    self.find_additions(sentence, node, idx, RESULT_LEN - len(completions)),
                    self.find_removals(sentence, node, idx)
                ]
                for result, current_node in results:
                    completions += self.format_result(result, completions_sentences,
                                                          base_scores - self.decrement_scores["search_replaced"][idx])
                    if len(completions) >= RESULT_LEN:
                        return completions[:RESULT_LEN], current_node

        return completions[:RESULT_LEN], current_node

    def format_result(self, result, completions_sentences, scores):
        """
        Formats the result to include additional data such as the source and score for each suggestion.
        Ensures that duplicate sentences are not included in the final list of suggestions.
        """
        formatted_results = []
        for index, (sentence_idx, occurrence_idx) in enumerate(result.items()):
            if len(formatted_results) >= RESULT_LEN - len(completions_sentences):
                break
            sentence, sentence_data = self.data_manager.fetch_sentence_data(sentence_idx)
            if sentence not in completions_sentences:
                formatted_results.append(
                    f"{sentence} ({sentence_data}, occurrence index: {occurrence_idx}) score: {scores}")
                completions_sentences.append(sentence)
        return formatted_results
