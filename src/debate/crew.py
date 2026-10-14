from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model="deepseek-v4-flash",
    base_url="https://api.mixroute.ai/v1",
    api_key=os.getenv("MIXROUTE_API_KEY")
)
llm1 = LLM(
    model="gemini-3.5-flash-lite",
    base_url="https://api.mixroute.ai/v1",
    api_key=os.getenv("MIXROUTE_API_KEY")
)

@CrewBase
class Debate():
    """Debate crew""" 

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config['debater'],
            llm = llm, 
            verbose=True
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'],
            llm = llm1, 
            verbose=True
        )


    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'], 
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'],
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config['decide'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
