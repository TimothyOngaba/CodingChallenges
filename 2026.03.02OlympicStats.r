"Task
Explore the dataset for associations between variables. Exemplar questions include: 
Who is the most decorated Olympian? 
What country has the most medals?
Does the host country have an advantage? 
When were women allowed to compete and what countries sent female athletes in this first game? 
Do taller athletes do better in certain events?"

#Reading in the data
library(readr)
athlete_events <- read_csv("UAEPlacement/CodingChallenges/athlete_events.csv/athlete_events.csv", 
                            col_types = cols(Age = col_integer(), 
                            Height = col_integer(), Weight = col_integer(), 
                            Year = col_number()))

#Determining most decorated athlete
library(dplyr)
athlete_events %>%
  filter(!is.na(Medal)) %>%   # Removes non-medal rows
  group_by(Name) %>%
  summarise(
    gold   = sum(Medal == "Gold"),
    silver = sum(Medal == "Silver"),
    bronze = sum(Medal == "Bronze"),
    total_medals = n(),
    .groups = "drop"
  ) %>%
  arrange(desc(total_medals)) %>%
  slice(1)
# Country with most medals
athlete_events %>%
  filter(!is.na(Medal)) %>%   # Remove non-medal rows
  group_by(NOC) %>%
  summarise(
    gold   = sum(Medal == "Gold"),
    silver = sum(Medal == "Silver"),
    bronze = sum(Medal == "Bronze"),
    total_medals = n(),
    .groups = "drop"
  ) %>%
  arrange(desc(total_medals)) %>%
  slice(1)
# Host country advantage
# get last 15 games
last_15_games <- athlete_events %>%
  distinct(Games, Year, City) %>%
  arrange(desc(Year)) %>%
  slice_head(n = 15)

# calculate medals them 15 games
medals_last_15 <- athlete_events %>%
  filter(!is.na(Medal)) %>%
  semi_join(last_15_games, by = c("Games", "Year", "City")) %>%
  group_by(Games, Year, City, NOC) %>%
  summarise(total_medals = n(), .groups = "drop")
# find top country by host city
top_country_by_city <- medals_last_15 %>%
  group_by(Games, Year, City) %>%
  slice_max(total_medals, n = 1, with_ties = FALSE) %>%
  ungroup()
# display results
top_country_by_city %>%
  mutate(
    Games_Label = paste0(City, " (", Year, ")")
  ) %>%
  select(Games_Label, NOC, total_medals)

# Determining when women were allowed to compete and countries that sent female athletes in these first games
athlete_events %>%
  filter(Sex == "F") %>%
  arrange(Year) %>%
  slice(1) %>%
  select(Games, Year, City)
first_female_info$Year

athlete_events %>%
  filter(Sex == "F", Year == first_year) %>%
  distinct(NOC, Team) %>%
  arrange(NOC)

# Do taller athletes do better in certain events?
athlete_events %>%
  filter(!is.na(Medal), !is.na(Height)) %>%
  group_by(Sport) %>%
  summarise(
    avg_height_medalists = mean(Height, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(avg_height_medalists))