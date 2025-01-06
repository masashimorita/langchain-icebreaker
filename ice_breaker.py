from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser


def ice_break_with(name: str, mock: bool = False) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    print(linkedin_username)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=mock)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=mock)
    print(twitter_username)
    print(tweets)

    summary_tempalte = """
        given the information about a person from LinkedIn {information},
        and their latest twitter posts {twitter_posts} I want you to create:
        1. a short summary
        2. two interesting facts about them

        Use both information from twitter and Linkedin
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_tempalte,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser
    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    print(res)


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")

    ice_break_with(name="Eden Marco Udemy", mock=True)
