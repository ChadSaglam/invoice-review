from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class InvoiceReview:
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def invoice_classifier(self) -> Agent:
        return Agent(config=self.agents_config["invoice_classifier"], verbose=True)

    @agent
    def vat_checker(self) -> Agent:
        return Agent(config=self.agents_config["vat_checker"], verbose=True)

    @agent
    def review_reporter(self) -> Agent:
        return Agent(config=self.agents_config["review_reporter"], verbose=True)

    @task
    def classify_task(self) -> Task:
        return Task(config=self.tasks_config["classify_task"])

    @task
    def vat_task(self) -> Task:
        return Task(config=self.tasks_config["vat_task"])

    @task
    def report_task(self) -> Task:
        return Task(config=self.tasks_config["report_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks,
                    process=Process.sequential, verbose=True)