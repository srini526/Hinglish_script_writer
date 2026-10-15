import os
from typing import TypedDict

# lets create the state

class pipelinestate(TypedDict):
    raw_input : str
    edited_text : str
    script_text : str
    final_output : str

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def build_pipeline():

    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)

    def editor_node(state : pipelinestate ) -> dict:
        """Stage 1 : Cleans up Grammer, removes typo, and refines the tone."""

        prompt = (
            "You are a expert Copyeditor. Clean up the following raw text"
            "Fix any grammatical errors, spelling mistakes, and smooth out the transition flow"
            "While keeping the core message intact. Return only edited text.\n\n"
            f"Text:\n{state["raw_input"]}"
        )
        response = llm.invoke(prompt)

        return {"edited_text" : response.content.strip()}

    def scriptwriter_node(state : pipelinestate) -> dict:
        """stage 2 : Formats the clean text into an engaging vedio script style."""
        print("\n--- [Stage 2] Executing Script Writer Node ---")

        prompt = (
            "You are a charismatic YouTube content creator. Take this edited text and transform "
            "it into a highly engaging, punchy, conversational video script hook. Make it sound "
            "like a real person speaking passionately. Return only the script content.\n\n"
            f"Edited Text:\n{state['edited_text']}"
        )
        response = llm.invoke(prompt)

        return {"script_text" : response.content.strip()}

    def translater_node(state : pipelinestate) -> dict:
        """stage 3 : Transalte the script into natural flowing Hinglish."""
        print("\n--- [Stage 3] Executing Translater Node ---")

        prompt = (
            "You are an expert content localizer for the Indian market. Take the following script "
            "and convert it into natural, flowing 'Hinglish'. Do not simply translate word-for-word "
            "or repeat information. Alternate comfortably between Hindi and English, just as "
            "an intellectual tech educator would speak naturally on a live stream. "
            "Return only the final Hinglish text.\n\n"
            f"Script:\n{state['script_text']}"
        )
        response = llm.invoke(prompt)

        return {"final_output" : response.content.strip()}


    # Now states and nodes are ready
    # Now time its time to create graph.
    # to curate the graph first we need to connect these nodes
    # for that u have to use edges
    # edges are very important to create workflows

    from langgraph.graph import StateGraph, START, END

    # create the graph 
    graph = StateGraph(pipelinestate)

    # add nodes to graph
    graph.add_node("editor", editor_node)

    graph.add_node("scriptwriter", scriptwriter_node)

    graph.add_node("translater", translater_node)


    # time to add edges (Sequential)

    graph.add_edge(START, "editor")
    graph.add_edge("editor", "scriptwriter")
    graph.add_edge("scriptwriter","translater")
    graph.add_edge("translater", END)


    # compile the graph

    return graph.compile()

# app = graph.compile()

# result = app.invoke({
#     "raw_input" : "Narrator: The old clockmaker fixed the golden watch, and time suddenly froze for everyone else. Leo: (Gasping) Why is the rain stopping in mid-air?  Narrator: He realized he now held the power to change history."
# })

# # Output
# print("You result is: \n\n")
# print(result['final_output'])


