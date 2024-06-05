
import os
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep

import streamlit as st

from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    SerperDevTool,
)


@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield





os.environ["OPENAI_MODEL_NAME"] ='gpt-3.5-turbo'  # Adjust based on available model

search_tool = SerperDevTool()

st.title('Legal Decision App')
example_case = st.text_area(
    'Enter case notes here', 
    "I am a tenant in NYC and I haven't had heat all winter. I contacted my landlord 3 times, but he hasn't responded and I have needed to buy a space heater to keep warm."
  )

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Legal Research Analyst',
  goal='Research the current case showing the evidence for and against it based on legal cases that were similar',
  backstory="""You work at a leading tenants rights law firm as a paralegal researcher
  you can comb through all cases in tenants law and identify the trends as to what cases
  are winning and what cases are losing. Your expertise lies in your ability to look over
  every detail for and against why a case is supported by evidence to make a clear case.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  max_iter = 100,
  tools=[search_tool, ]
)
lawyer = Agent(
  role='Tenants rights lawyer',
  goal='Make legal decisions to take a case or not based on whether it is a good enough case',
  backstory="""You are a renowned tenants rights lawyer, known for your ability to stand up for the
  rights of common people, but also to get paid well while doing it. You understand the power that 
  the warrant of habitability and rent abatement laws have if used correctly on the right cases. And 
  in these cases it really makes a difference. People can get the rent paid back up to several years 
  if the apartment is not deemed habitable. This can work out to a lump sum of a lot of money.
  
  You are trying to find good cases and so deciding whether the case in front of you is good or not
  is your main job. Also though, you need to compellingly present your case for why this case is good or not.
  """,
  verbose=True,
  allow_delegation=True,
  max_iter = 100,
)

# Create tasks for your agents
get_warrant_of_habitability_laws = Task(
  description="""Conduct a comprehensive investigation into the laws around 
  the warrant of habitability in New York City. Output all the requirements for a house to be 
  habitable with examples from specific cases""",
  expected_output="full description with lots of context and examples giving a very clear framework of the laws around what makes a house habitable",
  agent=researcher,
  output_file='cases/warrant_habitability_laws.md',
)

research_case = Task(
  description=f"""Here is an example of a tenant situation: {example_case}.
  Find 5 unique cases similar to this one in New York City to see how they were resolved.
  For each case, provide a summary of the case and whether the tenant won or lost the case.""",
  expected_output="a list of cases where each has the URL of the case, the name of the case, a case summary, and whether they won or lost.",
  agent=researcher,
  output_file='cases/cases.md',
)

judge_case = Task(
  description=f"""Look at the tenant situation: {example_case}.
  Based on the warrant of habitability and other example cases 
  develop legal advice on whether the case here would succeed or fail. 
  Be impartial and purely based on the facts and the laws and examples from other cases.
  Give the pros and cons of the case and the likelihood of winning or losing the case. 
  Link to helpful resources that can be used to support the case and link to examples of 
  cases that have been won or lost. Be concise and professional and don't make anything up
  that doesnt have a reference in a link provided.""",
  expected_output="Advice to the tenant with pros and cons on whether the current case probably would win or lose with links to resources and examples of similar cases.",
  agent=lawyer,
  context=[research_case],
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, lawyer],
  tasks=[judge_case],
  verbose=2, #You can set it to 1 or 2 to different logging levels
)
if st.button('Test Case'):
  # Get your crew to work!
  output = st.empty()
  with st_capture(output.code):
    result = crew.kickoff()

  st.write(result)
