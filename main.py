from auto_completion import AutoCompletion


def user_interface(auto_complete):
    """Get an input sentence from the user and print the completion suggestions.
          Type '#" to end the current input and start a new one, or 'exit' to quit the program."""
    print("Welcome to the Auto-Completion system!")
    print("Type your text and press enter for suggestions.")
    print("Type '#' at any time to end the current input and start anew, or type 'exit' to quit.")

    while True:
        _input = input("\nEnter your text here:\n").strip()
        if _input.lower() == "exit":
            print("Exiting the program...")
            break
        sentence = _input[:]
        node = auto_complete.data_manager.get_trie_structure().root
        while _input != "#":
            completions, node = auto_complete.aggregate_completions(sentence, node, len(sentence))
            if not len(completions):
                print("Sorry, no suggestions found. Type '#' to start a new input...")
            else:
                print(f"Here are {len(completions)} suggestions:")
                for i in range(len(completions)):
                    print(f"{i+1}. " + completions[i])
            print()
            _input = input(sentence)
            sentence += _input


if __name__ == '__main__':
    auto_complete = AutoCompletion()
    auto_complete.data_manager.initialize_data()
    user_interface(auto_complete)

