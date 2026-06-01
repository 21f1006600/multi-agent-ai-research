from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic : str) -> dict:

    state ={}   #kind of local storage

    #search_agent_working
    print("\n"+" ="*50)
    print("Search agent working...")
    print(" ="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")],
    })
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result", state["search_results"])

    #reader_agent_working
    print("\n"+" ="*50)
    print("Reader agent working...")
    print(" ="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
      "messages": [(
          "user",
          f"Based on the following search results about '{topic}', "
          f"pick the most relevant URL and scrape the information.\n\n"
          f"Search Results:\n{state['search_results'][:800]}"
      )]
})

    state["scraped_content"] = reader_result['messages'][-1].content

    print("\n scraped content: \n", state["scraped_content"])

    #-writer chain
    print("\n"+" ="*50)
    print("Writer chain working and drafting the report...")
    print(" ="*50)

    research_combined = (
        f"Search Results :\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}\n\n"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report:\n", state["report"])

    #critic report
    print("\n"+" ="*50)
    print("Critic chain reviewing the report...")
    print(" ="*50)

    state["feedback"] = critic_chain.invoke({
    "report": state["report"]
    })

    print("\n Critic Report:\n", state["feedback"])

    return state

if __name__ == "__main__":
    topic = input("Enter the topic: ")
    run_research_pipeline(topic)