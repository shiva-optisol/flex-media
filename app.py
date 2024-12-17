import streamlit as st
import asyncio
from gpt_researcher import GPTResearcher
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
# Function to get report from the backend
async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    
    # Get additional information
    research_context = researcher.get_research_context()
    # research_costs = researcher.get_costs()
    # research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()
    
    return report, research_context, research_sources

# Streamlit app code
def main():
    st.title("Product Research Assistant")

    # Input field for user query
    user_query = st.text_input("Enter your query")
    
    # Button to trigger the research
    if st.button("Get Research Report"):
        if user_query:
            with st.spinner("Processing your request..."):
                # Run the async function to get the report
                query = f"""Generate a detailed and cohesive market analysis report for '{user_query}'. The report should flow logically and combine related sections for clarity. Follow these guidelines:

Overview:
Summarize the product's key features, specifications, and qualities in a professional and concise manner.

Regional Performance & Trend Analysis:
Evaluate the product's sales performance across the USA, UK, and Middle Eastern markets (Saudi Arabia, UAE, and Egypt) without creating specific subtopics for locations. Identify trends in product demand, mentions, and availability gaps within these regions. Highlight key patterns such as unmet demand, seasonal trends, or supply issues. Provide actionable recommendations based on insights, like restocking high-demand areas or improving delivery infrastructure.

Quality Assessment & User Sentiment (UGC Analysis):
Provide a clear, crisp, and professional analysis of product quality based on user-generated content (UGC) and expert reviews. Analyze content such as customer reviews, forum discussions, and social media mentions. Include:

Sentiment analysis: Classify user feedback into positive, negative, or neutral categories.
Key themes: Identify recurring issues (e.g., pricing concerns, quality complaints) and positive aspects (e.g., features, durability).
Summarized insights: Provide concise and actionable conclusions without creating subtopics.
Comparison Table Across E-Commerce Platforms:
Create a table comparing the product across different websites. Only include websites that have information about the product. The table should include the following columns:
| Website | Product Name | Price | Discount | User Rating | Number of Reviews | Shipping Options | Stock Availability | Return Policy | Seller Name/Verified | Additional Perks |
Websites to consider: Amazon India, Flipkart, Myntra, Snapdeal, Tata CLiQ, AJIO, Paytm Mall, JioMart, Meesho, and IndiaMART.

Recommendations:
Offer actionable insights to improve product quality, address user concerns, and boost sales performance across all regions. Address availability gaps, optimize distribution, and align product features with user expectations.

Summary Table:
Summarize key findings in the following format:
| Region | Sales Performance | Quality Assessment | Top-Selling Factors | Underperformance Reasons |

References:
Professionally display links to relevant data sources at the end of the report. Ensure the references are neat, clear, and concise.

Note: Use information only from the following websites:
Amazon, Best Buy, CNET, TechRadar, PCMag, Wirecutter, Digital Trends, Tom's Guide, Reddit, Trustpilot, B&H Photo Video, Newegg, Amazon India, Flipkart, Myntra, Snapdeal, Tata CLiQ, AJIO, Paytm Mall, JioMart, Meesho, and IndiaMART."""
                report_type = "research_report"
                report, context, sources = asyncio.run(get_report(query, report_type))

                # Display the results
                st.subheader("Research Report:")
                st.write(report)

                # st.subheader("Research Context:")
                # st.write(context)

                # st.subheader("Research Costs:")
                # st.write(costs)
                # if images:
                #     st.subheader("Research Images:")
                # for img in images:
                #     st.image(img, use_column_width=True)

                # st.subheader("Research Sources:")
                # st.write(sources)
        else:
            st.error("Please enter a valid query.")

if __name__ == "__main__":
    main()
