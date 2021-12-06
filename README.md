![Banner](League_logo.jpeg)

# League of Legends Capstone

<!-- Add buttons here -->

https://user-images.githubusercontent.com/85950629/142899692-a7a8c0d5-4594-428e-9f8e-d0a8de370863.mp4

![A-Map-of-the-League-of-Legends-game-play-in-the-classic-mode](https://user-images.githubusercontent.com/85950629/142907747-8a78835d-1d6b-4877-8d02-eaed5ec6f25d.png)


![GitHub release (latest by date including pre-releases)](https://img.shields.io/badge/release-draft-yellow)
![GitHub last commit](https://img.shields.io/badge/last%20commit-Oct%202021-green)

<!-- Describe your project in brief -->
Link to where we acquired the original dataset from: (https://developer.riotgames.com/)
# Project Summary
Esports is a booming global industry that will soon rival that of traditional professional sports. League of Legends is one of the largest esports in the world that generated $1.75 billion dollars for Riot Games in 2020 alone. A professional match can last around 20 minutes, and we've created a model that predicts the winner of a match by 10 minutes. This can be utilized by professional analysts of the game, applied to other sports, and help game developers discover any imbalances of the game mechanics.



# Executive Summary
<!-- Add a demo for your project -->

### Project Goals
- Create a model that will predict the probability of winning for each team by the 10 minute mark of a League of Legends match using live data obtained Riot’s api on the newest seasons patch 11.23.

### Data summary
- The data is only from the north American Server
- The data contains pro players, and other top performers of the game, The lowest ranking players are in masters, which is still the top .15% of players.
- This data comes from the latest patch of league of legends, Patch 11.23

The data was pulled from the riot api using names that were gathered from webscraping two popular League of legends sites called **op.gg** (https://na.op.gg/ranking/ladder/) and **trackingthepros** (https://www.trackingthepros.com/players/na/) op.gg was used to grab roughly the top 5000 players in the ranked ladder, and trackingthepros was used to grab the names of the current professional league of legends players.



### Recommendations
Don't give away an early lead League of Legends is a very balanced game, and can swing into either teams favor. Focus your sights on dragons early and trying to get an experience lead on your enemy, and if you get your top laner ahead get rift heralds to push for early towers.

If your team is ahead of the other team focus on playing around your top laner, and tell your botside to play safe, and if you are behind focus on getting your bot lane ahead. This gives you your best chance of winning and turning the game around.



### Problem Statement
League of Legends is growing and with that comes increasing demands from coaches, analysts, casters, and the game developers. Coaches, analysts, and casters always need good data to make key decisions and develop better strategies and deeper understandings of what is the most important factors of a game. Game developers need to keep the game fair and fun, to continue developing their playerbase to stay at the top of esports and gaming popularity.

### Proposed solution
Create a machine learning model that can accuratly determine the team that will win based on certian features of a game, and what features have the largest impact on a teams success.

# Table of contents
<!-- Add a table of contents for your project -->

- [Project Title](#project-title)
- [Executive Summary](#executive-summary)
- [Table of contents](#table-of-contents)
- [League of legends Dictionary](#League-of-legends-dictionary)
- [Data Dictionary](#data-dictionary)
- [Data Science Pipeline](#data-science-pipline)
    - [Acquire](#acquire)
    - [Prepare](#prepare)
    - [Explore](#explore)
    - [Model](#model)
    - [Evaluate](#evaluate)
- [Conclusion](#conclusion)
- [Given More Time](#given-more-time)
- [Recreate This Project](#recreate-this-project)
- [Footer](#footer)

# League of Legends Common Termonology
[(Back to top)](#table-of-contents)
<!-- Drop that sweet sweet dictionary here-->

| League terms    | Plain explination                                               | 
|:----------------|:----------------------------------------------------------------|
| Riot            |Riot games is the company that owns league of legends.           |
| Kill            |Given to the player that deals the final blow. Rewards gold.     |
| Assist          |Given to the player(s) that help in a kill. Rewards some gold.   |
| Death           |When players lose all health. Temporarily taken out of game.     |
| Level           |Each level makes your character stronger. Max level: 18.         |
| Experience(xp)  |Used to level up.Experienced gained for being near the action.   |
| Dragon          |A neutral monster that both teams can take. Gives bonuses.       |
| herald          |A neutral monster that both teams can take. Takes towers.        |
| Baron           |A neutral monster that both teams can take. Gives bonuses.       |
| Champion        |A playable character in League of legends.                       |
| Summoner        |A name for the players, each player is a summoner.               |
| Summoners rift  |The map that competative games of league are held on.            |
| Lane            |There are three lanes on summoners rift and each has differences.|
| Jungle          |A role that has no lane but assists the other lanes.             |
| Minion          |Small ai controlled fighters that give gold when killed.         |
| Monster         |Normally stronger then minions they spawn in the jungle.         |
| Tower           |A structure in the game that defends itself.                     |
| Wards           |An item that gives vision in the jungle, and in bushes.          |
| Crowd Control   |A structure in the game that defends itself.                     |
| Inhibitor       |A structure that when taken strengthens the other teams minions. |
| Nexus           |Goal of players to take the enemy nexus. How you win.            |
| Abilities       |spells or special moves given to each character.                 |
| Gold            |Players get gold by killing things on the map.                   |
| Items           |Players use gold to buy items to make themselves stronger.       |
| Armor           |Reduces damage from physiscal attacks.                           |
| Magic Resist    |Reduces damage from magic attacks.                               |
| Magic damage    |Increases damage of abilities, and sometime attacks.             |
| Physical damage |Increses damage of attacks, and sometimes abilities.             |
| True Damage     |Ignores armor and magic resist.                                  |
| Blue Team       |Blue team starts the game at the bottom left.                    |
| Red Team        |Red team starts the game at the top right.                       |
| puuid           |An encrypted id given to each player on the riot api.            |

# Data Dictionary
[(Back to top)](#table-of-contents)
<!-- Drop that sweet sweet dictionary here-->

| Feature                    | Datatype                | Definition   |
|:----------------------|:------------------------|:-------------|
| BlueTeamTotalGoldDifference|int64|Gives the difference in gold between teams|
| BlueTeamLevelDifference|int64|Gives the difference in level between teams|
| BlueTeamXpDifference|int64|Gives the difference in expererience between teams|
| BlueTeamWardDifference|int64|Gives the difference in wards between teams|
| BlueTeamMinionKillDifference|int64|Gives the difference in minions killed between teams|
| BlueTeamDeathsDifference|int64|Gives the difference in deaths between teams|
| BlueTeamMagicDmgDifference|int64|Gives the difference in magic damage between teams|
| BlueTeamPhysicalDmgDifference|int64|Gives the difference in physical damage between teams|
| BlueTeamTrueDmgDifference|int64|Gives the difference in true damage between teams|
| BlueTeamTotalDmgDifference|int64|Gives the difference in total damage between teams|
| BlueTeamTotalMinionsMonstersDifference|int64|Gives the difference in monsters and minion kills|
| BlueTeamTimeCCingDifference|int64|Gives the difference in time croud controling between teams|
| BlueTeamWaterDragonDifference|int64|Gives the difference in water dragons between teams|
| BlueTeamAirDragonDifference|int64|Gives the difference in air dragons between teams|
| BlueTeamChemtechDragonDifference|int64|Gives the difference in chemtech dragons between teams|
| BlueTeamFireDragonDifference|int64|Gives the difference in fire dragons between teams|
| BlueTeamHextechDragonDifference|int64|Gives the difference in hextech dragons between teams|
| BlueTeamEarthDragonDifference|int64|Gives the difference in earth dragons between teams|
| BlueTeamKdaDifference|int64|Gives the difference in KDA between teams|

# Data Science Pipeline
[(Back to top)](#table-of-contents)
<!-- Describe your Data Science Pipeline process -->
Following best practices I documented my progress throughout the project and will provide quick summaries and thoughts here.

### Planning
- Communicate with teammates about strengths and weaknesses to find team members that can lead specific sections in the work.
- Clearly outline and define our goal as being a teams chance of winning at the 10 minute mark in a league of legends game.
- Build out a trello board that the team can reference that contains an outline of information we will use when completing the rest of the datascience pipeline.

**Link to Trello board** : https://trello.com/b/lW8DJA3k/project-planning


### Acquire
[(Back to top)](#table-of-contents)
<!-- Describe your acquire process -->
- Webscraped two sites to gather summoner names (username) for the Riot games developer api.
- Used the summoner names to get a unique puuid, which is league of legends unique identifier for players.
- Using the puuid we were able to get the matchid's of the last 100 games for each of the players.
- After we had the matchid's we pulled in json files for each match and the timeline of events that happened in the match.
### Prepare
[(Back to top)](#table-of-contents)
<!-- Describe your prepare process -->
- From json files that were gathered from the Riot api, functions were created that would build a dataframe of both team, and individual stats from the 10 minute mark.
- Columns were renamed to change the team id's of 100 to blue and 200 to red.
- Replaced nulls with zero.
- Split data for exploration.

**Feature Engineering**

- Created varies difference columns for (blue team column) - (red team column)
- MVP stats
- KDA (kills * 1.75) (deaths) (assists * .5)


### Explore

- Hypothesis 1: We reject the null hypothesis.
    - alpha: 0.05
    - Null Hypothesis: Blue team's gold difference over 40 and blue team's Xp over 17k  is not significant
    - Alternative Hypothesis: Blue team's gold difference over 40 and blue team's Xp over 17k  is  significant
- Hypothesis 2: We reject the null hypothesis.
    - alpha: 0.05
    - Null Hypothesis: Blue team's physical damage difference over -85 and blue team's kda difference over 0 is not significant
    - Alternative Hypothesis: Blue team's physical damage difference over -85 and blue team's kda difference over 0  is significant
- Hypothesis 3: We fail to reject the null hypothesis.
    - alpha: 0.05
    - Null Hypothesis: Blue team's ward difference over 0 and blue team's minion kills difference over 0  is not significant
    - Alternative Hypothesis: Blue team's ward difference over 0 and blue team's minion kills difference over 0  is  significant


[(Back to top)](#table-of-contents)
<!-- Describe your explore process -->
- Goal: Visualize the data and explore possible relationships. The use of visuals and statistics tests aided in the help to answer my questions. 
**Hypothesis**
1. Will Blue team's gold difference over 40 and blue team's Xp under 17k be significant?
2. Is there a difference in the outcome of the game if blue team’s physical damage difference and the team’s kda difference is over the mean?
3. Does the blue team’s wards difference and the team minion kills difference factor into the outcome of the game at the 10 minute mark? 


#### Statistical testing:
- There was a low correlation of -.03 blue team total gold difference and the result of the game
- We are 95% confident that there is evidence to suggest Blue team's physical damage difference over -85 and blue team's kda difference over 0 is significant with a p value of .01


### Model
[(Back to top)](#table-of-contents)
<!-- Describe your modeling process -->
- Split the data into X and y groups and into train and test datasets.
- Utilized cross validation and grid search.
- Created optimized random forest classifier.
- Refit the best performing model on our entire train dataset.

**Model accuracy**

- ~95% mean cross validation accuracy.
- Refit the best performing model on our entire train dataset.

### Evaluate
[(Back to top)](#table-of-contents)
<!-- Describe your evaluation process -->
**Test Accuracy**
- Models accuracy on test data: ~61.15%
**Test Precision**
- Models precision on test data: ~63%
**Test Recall**
- Models Recall on test data: ~57%
**F1-Score**
- Models F1-score on test data: ~60%
**Support**
- Models support for test data: 497
# Conclusion
[(Back to top)](#table-of-contents)
<!-- Wrap up with conclusions and takeaways -->
League of legends is a balanced game, even if you fall behind early, a comeback is still well within reach.
# Given More Time/ Next steps
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHAT YOU WISH YOU COULD HAVE DONE-->
- Make a live dashboard that updates every 5 minutes updating the chances of winning.
- Pull players from all ranks and perform the same analysis.
# Recreate This Project
[(Back to top)](#table-of-contents)
<!-- How can they do what you do?-->
- Make a copy of our final.csv in order to avoid acquiring through the riot api.
- Use the rename_cols function in our prepare.py.
- Continue working though the project using the functions created to help along the way.
# Footer
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHO YOU ARE (linkedin links) close with a joke. -->

#### Individual team members github links:
- **Chris Everts**: https://github.com/chriseverts
- **Johnathon Smith**: https://github.com/johnathon-smith
- **Joshua Bryant**: https://github.com/Joshua-C-Bryant
- **Joshua Chaves**: https://github.com/joshuamchavez2
- **Jared Vahle**: https://github.com/JaredVahle

#### Individual team members linkedin links:
- **Chris Everts**: https://www.linkedin.com/in/chris-everts
- **Johnathon Smith**: https://www.linkedin.com/in/smith-johnathon/
- **Joshua Bryant**: https://www.linkedin.com/in/joshcbryant/
- **Joshua Chaves**: https://www.linkedin.com/in/joshuamchavez2/
- **Jared Vahle**: https://www.linkedin.com/in/jared-vahle-data-science/
