Auto-Completion Sentence Project for Google Search Enhancement
Overview
The Auto-Completion Sentence Project aims to enhance user experience on Google Search by providing real-time predictive text completions. This system leverages a sophisticated backend that dynamically handles user inputs to suggest the most relevant completions based on prior data compiled from various technical documents and articles.
Project Structure
Main Components
1. DataManager: Manages the lifecycle of sentence data, from extraction and loading from a ZIP file to structuring this data for efficient access and manipulation.
2. SentencesTrie: Implements a trie data structure to store sentences and allow for rapid retrieval based on prefixes and other criteria derived from user input.
3. AutoCompletion: Orchestrates the retrieval and ranking of sentence completions based on a blend of exact matches and fuzzy logic to handle typos or varied input formats.
Functional Workflow
- Initialization: Pre-loads and organizes data from specified sources into a manageable format, ensuring readiness for real-time user interaction.
- Completion Handling: Receives user inputs and processes them to suggest up to five of the most accurate completions, utilizing a combination of exact match and proximity calculations.
Getting Started
Prerequisites
- Python 3.6 or higher
- Access to the project’s ZIP file containing initial data (`Archive.zip`)
Installation
1. Clone the repository to your local machine.
2. Ensure the `Archive.zip` file is placed in the root directory of the project.
3. Install the necessary Python packages (if any are specified).
Running the Application
Execute the main script to start the application:
```bash
python main.py
```
Follow the on-screen prompts to type input text. Use "#" to reset the input process.
