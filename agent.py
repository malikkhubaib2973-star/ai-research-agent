from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import tool
from ddgs import DDGS


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return the top results."""
    try:
        results = DDGS().text(query, max_results=6)
    except Exception as e:
        return f"Search failed: {e}"
    if not results:
        return "No results found."
    return "\n\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}"
        for r in results
    )


def run_research(topic: str, api_key: str) -> str:
    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0.3,
    )

    researcher = Agent(
        role="Research Analyst",
        goal="Research any topic using web search and write a clear, accurate report",
        backstory="You are an expert analyst who finds reliable information and explains it simply.",
        tools=[web_search],
        llm=llm,
        max_iter=5,
        verbose=False,
    )

    task = Task(
    description=(
            "Research the topic: {topic}\n"
            "Use ONLY the 'Web Search' tool, 2-4 times with different queries. "
            "NEVER call any other tool such as web_open, browser, open_url or python. "
            "Do NOT try to open links; rely only on the search result summaries. "
            "After searching, write the final report directly."
        ),

        expected_output=(
            "A markdown report with: Title, Introduction, Key Findings (bullets), "
            "Detailed Analysis, Conclusion, and a Sources list with URLs."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )
    result = crew.kickoff(inputs={"topic": topic})
    return result.raw