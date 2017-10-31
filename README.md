# Identifying Power-Middle Influencers on Instagram
# Using Graph and Sentiment Analysis

## tl;dr
I identified the top power-middle influencers on Instagram using graph and sentiment analysis. Power-middle influencers have a devoted following and tend to have a higher interaction rate with their followers, and therefore can make more authentic and affordable endorsements of niche products.

## File Structure Summary 
Directory | Description
------------ | -------------
data | selected graphs and dictionaries used in this project
graph_util | scripts for creating graphs and calculating centralities
images | EDA and README figures
src | script for pipeline to calculate top influencers
webscrape_util | scripts for requesting/scraping the GraphQL API

## Business Question

If a company is marketing a niche product, it may not be a wise idea to request promotion from someone with a large (millions) social media following - it is clear that they have been solicited to sponsor certain brands or items, and therefore seems less authentic. To market to a smaller audience, it may be more affordable and effective to identify a “power-middle” influencer, who would be able to market to a smaller, intimate audience. These influencers will be more influential to the smaller but more loyal following they have amassed. How do you find power-middle influencers who will be the most influential to the group of people you are trying to target?


## Data Understanding and Preparation

### General Outline of Data Collection:
 - First, I choose a community, take female climbers for instance.
 - Then, I have to identify potential power-middle influencers; I did this by finding people who posted content with the hashtag #womenwhoclimb on Instagram (using requests).
 - I estimated the rest of the community by finding people who followed these potential influencers (using selenium).

### Conceptualization:
A social network graph (Digraph in NetworkX) is constructed using the influencers and followers. This graph can be used to identify power-middle influencers and other interesting features about the community.
* Number of nodes: 2268840
* Number of edges: 3582464


## Modeling

Graph clustering using NetworkX to find influencers and communities. Various centrality measures are calculated to explore influencers’ roles in the social network.

## Evaluation
Unsupervised learning approaches will be used to search for influencers and communities.

Performance will be evaluated by checking if top influencers via graph analysis are already sponsored. Top influencers on the graph analysis leaderboard will be compared to the “top results” on the Instagram search page.
