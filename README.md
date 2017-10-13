# Targeting Power Middle Influencers


## Business Understanding

If a company is marketing a niche product, it may not be a wise idea to request promotion from someone with a large social media following - it is clear that they have been solicited to sponsor certain brands or items, and therefore seems less authentic. To market to a smaller audience, it may be wiser to target a “power-middle” influencer, who would be able to market to a smaller, intimate audience. These influencers will be more cost-effective, and will be more influential to the smaller but more loyal following they have amassed. How do you find power-middle influencers who will be the most influential to the group of people you are trying to target?


## Data Understanding
To narrow the scope of the problem, I narrow it down to one subject; products for female climbers. I scrape Instagram using [selenium and the request module].

General Outline of Data Collection:
 - Search hashtag and amass all people who have used this hashtag, or “influencers”
 - Find either or both:
      * People who have “liked” the photo with the specific hashtag
      * People who “follow” the influencer

### Conceptualization:
A social network graph is constructed using the influencers and followers. This graph can be used to identify power middle influencers and other interesting features about the community.

## Data Preparation
 - Nodes: influencers and followers.
 - Edges: following or liking.  

## Modeling
Graph clustering using NetworkX to find influencers and communities. Various centrality measures are calculated to explore influencers’ roles in the social network.

## Evaluation
Unsupervised learning approaches will be used to search for influencers and communities.

Performance will be evaluated by checking if top influencers via graph analysis are already sponsored. Top influencers on the graph analysis leaderboard will be compared to the “top results” on the Instagram search page.
