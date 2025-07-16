from crewai import Agent,Task,Crew  
from crewai import LLM
import requests
from bs4 import BeautifulSoup


llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)


resumer = Agent(
    role='Expert Content Summarizer',
    goal='Generate accurate, concise, and insightful summaries from long-form web content, focusing on clarity and essential information.',
    backstory='A seasoned analyst with deep expertise in natural language understanding and information distillation. Known for transforming complex texts into digestible and structured summaries for decision-makers, researchers, and the general public.',
    llm = llm,
    allow_delegations=False,
)


reviewer = Agent(
    role='Critical Review Analyst',
    goal=(
        'Carefully review the summary provided by the Summarizer agent. '
        'Ensure that the most important information is preserved, the tone is neutral, and the structure is coherent. '
        'If improvements are needed, return constructive feedback to the Summarizer agent.'
    ),
    backstory=(
        'A meticulous editorial reviewer with years of experience refining analytical and educational content. '
        'Trained to identify missing key points, vague statements, and structural issues in summaries, always aiming to improve clarity and reliability.'
    ),
    llm = llm,
)


def extract_text_from_url(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        tag.decompose()

    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text.strip()


def summarize_and_review(url: str) -> dict:
    article_text = extract_text_from_url(url)
    if article_text.startswith("ERROR"):
        return {"error": article_text}

   
    truncated_text = article_text[:8000]

    resumer_task = Task(
            description=(
            f"Analyze the following article content and generate a highly concise, well-structured, and objective summary:\n\n"
            f"---ARTICLE CONTENT START---\n{truncated_text}\n---ARTICLE CONTENT END---\n\n"
            "Your summary MUST capture the main arguments, key facts, and conclusions. "
            "**DO NOT RESPOND WITH ANYTHING OTHER THAN THE FINAL SUMMARY.**\n"
            "DO NOT SAY OKAY, OR EXPLAIN ANYTHING, OR EVEN INTRODUCE THE ANSWER.\n"
            "ONLY RETURN THE SUMMARY TEXT.\n\n"
            "It should be easily understandable by a general audience, free of jargon, and maintain a strictly neutral tone. "
            "Focus on extracting the most critical information, avoiding any personal opinions or interpretations. "
            "The summary should ideally be between 3 to 5 paragraphs, or approximately 150-250 words, focusing on the core message.\n\n"
            "**IMPORTANT: Your final output MUST BE ONLY the generated summary text, with NO conversational filler, no introductions, no conclusions, and no extra text whatsoever. Just the summary itself.**"
        ),
        expected_output="A concise, well-organized summary (3-5 paragraphs) highlighting main arguments, key facts, and conclusions, written in a neutral tone.",
        agent=resumer,
    )

    reviewer_task = Task(
        description=(
            "You are tasked with critically reviewing the summary provided as input. "
            "Your objective is to ensure its accuracy, completeness of key information, neutrality, clarity, coherence, and conciseness.\n\n"
            "**The summary to review is provided directly as your input from the previous task.**\n\n"
            "Based on your rigorous review of THIS provided summary, create the FINAL, polished version. "
             "Your summary MUST capture the main arguments, key facts, and conclusions. "
            "**DO NOT RESPOND WITH ANYTHING OTHER THAN THE FINAL SUMMARY.**\n"
            "DO NOT SAY OKAY, OR EXPLAIN ANYTHING, OR EVEN INTRODUCE THE ANSWER.\n"
            "ONLY RETURN THE SUMMARY TEXT.\n\n"
            "If the input summary is already excellent, simply return it as is. If improvements are needed, revise it to meet all the criteria. "
            "**IMPORTANT: Your final output MUST BE ONLY the fully revised and polished summary text, ready for publication, with NO additional conversation, thoughts, or introductory/concluding remarks. Just the final summary itself.**"
        ),
        expected_output="The FINAL, polished, and thoroughly reviewed version of the summary, ensuring accuracy, completeness of key information, neutrality, clarity, coherence, and conciseness.",
        agent=reviewer,
    )

    crew = Crew(
        agents=[resumer, reviewer],
        tasks=[resumer_task, reviewer_task],
        verbose=True
    )

    summary_result = crew.kickoff()

    return {
    "summary": summary_result.raw
}
