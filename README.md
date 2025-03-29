
=======
# CrewAI Streamlit Research Assistant

This project demonstrates how to build an end-to-end application using CrewAI and Streamlit. The application creates a team of AI agents that work together to research topics, write reports, and review content.

## Features

- **Multi-agent collaboration**: Uses three specialized agents (Researcher, Writer, and Reviewer)
- **Interactive web interface**: Built with Streamlit for easy user interaction
- **Research workflow**: Performs research, report writing, and content review in sequence
- **Download reports**: Save the final research reports as markdown files

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)
3. Enter your OpenAI API key and research topic
4. Click "Start Research Process" to begin

## How It Works

The application uses CrewAI to orchestrate three AI agents:

1. **Researcher Agent**: Gathers information on the specified topic
2. **Writer Agent**: Creates a structured report based on the research
3. **Reviewer Agent**: Checks the report for accuracy and clarity

Each agent completes its task in sequence, passing the results to the next agent.

## Customization

You can modify the agents' descriptions, goals, and tasks in the `app.py` file to suit your specific needs. You can also add more agents to the crew for more complex workflows.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
>>>>>>> 0eb78a8 (project code updated)
