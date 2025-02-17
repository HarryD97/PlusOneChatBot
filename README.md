# Compare different Structure
1. ChatGPT Model
2. RAG + LangChain ChatGPT
# RAG + LangChain ChatGPT
## Cost
1. OpenAI key token
2. Pinecone Key
3. (Potential) Google Customized Searching API
## Implementation Detail
### Data Collection
#### Source 
1. Crawl All the text content from 'https://www.plusonefoundation.org/'
2. Documentation (PDF, DOC, TXT...)
3. Google Customized search
#### What to improve
1. Improve the quality of the data (for demo, I collected all character, but need to remove the text that occur on every webpage)
2. Using nonstructual Database ( MongoDB...) may help organize data
3. use some webdriver to crawl them dynamic datas(if there are) on the website
4. Split the sources for different visiter
    1. people need help
    2. want to donate
    3. Support Different Language
    4. ...
5. ...

### Embeddings
#### What to improve
1. find better embeddings algorithm
2. find the best chunk size for the documentation

### ChatBot
#### ChatGPT-3.5-Turbo
#### What to improve
1. using GPT4o may have better performance but cost more money
2. Refine the prompt to have better effect

### Overal Routine
#### What's next
1. Clean the data to have better embeddings
2. Make the ChatBot more intellegent
3. Cache different user's history conversation
    1. using cookie or other token for cache
    2. store overtime conversation history
4. Deploy on a platform that can embeded in our Website.
# Prompting Tips
1. Encouraging Factual Accuracy: Asking to cite sources is an example to not let the LLM ``hallucinate'' responses
2. ...
