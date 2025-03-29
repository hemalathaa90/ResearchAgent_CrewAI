import streamlit as st
import os
from crewai import Agent, Task, Crew
from openai import OpenAI

st.set_page_config(page_title="CrewAI Research Assistant", page_icon="🤖", layout="wide")

# Title and description
st.title("CrewAI Research Assistant")
st.markdown("""
This application uses CrewAI to create a team of AI agents that work together to research topics,
write reports, and review the final content. Enter your OpenAI API key and a research topic to get started.
""")

# API Key input
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Topic input
research_topic = st.text_input("Enter a research topic", value="Latest advancements in AI")

# Add tabs for different sections
tab1, tab2, tab3 = st.tabs(["Research Process", "Results", "About"])

with tab1:
    st.header("Research Process")
    
    # Initialize session state variables if they don't exist
    if 'process_started' not in st.session_state:
        st.session_state.process_started = False
    if 'research_done' not in st.session_state:
        st.session_state.research_done = False
    if 'report_written' not in st.session_state:
        st.session_state.report_written = False
    if 'review_done' not in st.session_state:
        st.session_state.review_done = False
    if 'research_output' not in st.session_state:
        st.session_state.research_output = ""
    if 'report_output' not in st.session_state:
        st.session_state.report_output = ""
    if 'review_output' not in st.session_state:
        st.session_state.review_output = ""
    
    def reset_states():
        st.session_state.process_started = False
        st.session_state.research_done = False
        st.session_state.report_written = False
        st.session_state.review_done = False
    
    # Start process button
    if st.button("Start Research Process"):
        if not api_key:
            st.error("Please enter your OpenAI API key first.")
        else:
            with st.spinner("Setting up the research crew..."):
                st.session_state.process_started = True
                st.success("Research crew has been assembled!")
    
    # Display process status
    if st.session_state.process_started:
        st.subheader("Current Status:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("Researcher Agent")
            if st.session_state.research_done:
                st.success("Research completed ✅")
            else:
                with st.spinner("Researching..."):
                    # Set up OpenAI API
                    os.environ["OPENAI_API_KEY"] = api_key
                    
                    # Create the researcher agent
                    researcher = Agent(
                        name="Researcher",
                        description=f"An AI agent that researches and gathers information on {research_topic}.",
                        goal=f"Find relevant information on {research_topic}.",
                        role="Researcher",
                        backstory="An AI assistant designed for research tasks."
                    )
                    
                    # Create research task
                    research_task = Task(
                        name="Gather Information",
                        description=f"Find the latest information on {research_topic} and summarize key findings.",
                        agent=researcher,
                        expected_output=f"A summary of key findings about {research_topic}."
                    )
                    
                    # Initialize crew with researcher
                    research_crew = Crew(agents=[researcher], tasks=[research_task])
                    result = research_crew.kickoff()
                    
                    # Store the research output as a string
                    st.session_state.research_output = str(result)
                    st.session_state.research_done = True
                    st.success("Research completed ✅")
        
        with col2:
            st.info("Writer Agent")
            if st.session_state.research_done and not st.session_state.report_written:
                with st.spinner("Writing report..."):
                    # Create the writer agent
                    writer = Agent(
                        name="Writer",
                        description="An AI agent that writes research reports.",
                        goal=f"Create a structured report on {research_topic} from gathered research data.",
                        role="Writer",
                        backstory="An AI assistant designed for writing reports."
                    )
                    
                    # Create writing task
                    write_task = Task(
                        name="Write Research Report",
                        description=f"Use the following research to create a structured report on {research_topic}: {st.session_state.research_output}",
                        agent=writer,
                        expected_output=f"A structured research report on {research_topic}."
                    )
                    
                    # Initialize crew with writer
                    writing_crew = Crew(agents=[writer], tasks=[write_task])
                    result = writing_crew.kickoff()
                    
                    # Store the report output as a string
                    st.session_state.report_output = str(result)
                    st.session_state.report_written = True
                    st.success("Report written ✅")
            elif st.session_state.report_written:
                st.success("Report written ✅")
            else:
                st.info("Waiting for research to complete...")
        
        with col3:
            st.info("Reviewer Agent")
            if st.session_state.report_written and not st.session_state.review_done:
                with st.spinner("Reviewing report..."):
                    # Create the reviewer agent
                    reviewer = Agent(
                        name="Reviewer",
                        description="An AI agent that reviews and refines reports.",
                        goal="Ensure clarity, grammar, and accuracy in written content.",
                        role="Reviewer",
                        backstory="An AI assistant designed for reviewing reports."
                    )
                    
                    # Create review task
                    review_task = Task(
                        name="Review Report",
                        description=f"Review the following report on {research_topic} for accuracy and clarity: {st.session_state.report_output}",
                        agent=reviewer,
                        expected_output=f"A reviewed and refined research report on {research_topic}."
                    )
                    
                    # Initialize crew with reviewer
                    review_crew = Crew(agents=[reviewer], tasks=[review_task])
                    result = review_crew.kickoff()
                    
                    # Store the review output as a string
                    st.session_state.review_output = str(result)
                    st.session_state.review_done = True
                    st.success("Review completed ✅")
            elif st.session_state.review_done:
                st.success("Review completed ✅")
            else:
                st.info("Waiting for report to be written...")
        
        # Reset button
        if st.session_state.review_done:
            if st.button("Start New Research"):
                reset_states()
                st.experimental_rerun()

with tab2:
    st.header("Research Results")
    
    if st.session_state.research_done:
        st.subheader("Research Findings")
        st.markdown(st.session_state.research_output)
    
    if st.session_state.report_written:
        st.subheader("Written Report")
        st.markdown(st.session_state.report_output)
    
    if st.session_state.review_done:
        st.subheader("Final Reviewed Report")
        st.markdown(st.session_state.review_output)
        
        # Download button for the final report - using string instead of CrewOutput object
        st.download_button(
            label="Download Final Report",
            data=st.session_state.review_output,
            file_name="research_report.md",
            mime="text/markdown"
        )
    
    if not st.session_state.research_done:
        st.info("Start the research process to see results here.")

with tab3:
    st.header("About CrewAI")
    st.markdown("""
    ## What is CrewAI?
    
    CrewAI is a framework for orchestrating role-playing, autonomous AI agents. By working together in a crew, these agents can tackle complex tasks through collaboration.
    
    ## Key Components
    
    1. **Agents**: AI entities with specific roles, goals, and backstories
    2. **Tasks**: Specific assignments given to agents
    3. **Crew**: A team of agents working together to accomplish tasks
    
    ## How It Works
    
    In this application:
    - The **Researcher** agent gathers information on your topic
    - The **Writer** agent creates a structured report from the research
    - The **Reviewer** agent checks the report for accuracy and clarity
    
    Learn more at [CrewAI's official documentation](https://docs.crewai.com/introduction)
    """)