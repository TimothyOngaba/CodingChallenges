"""
Challenge questions
Who is the best team of all time?
Which teams dominated different eras of football?
What trends have there been in international football throughout the ages - home advantage,
total goals scored, distribution of teams' strength etc?
Can we say anything about geopolitics from football fixtures - how has the number of countries
changed, which teams like to play each other?
Which countries host the most matches where they themselves are not participating in?
How much, if at all, does hosting a major tournament help a country's chances in the
tournament?
Which teams are the most active in playing friendlies and friendly tournaments - does it help or
hurt them?
"""

#loading relevant libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(lubridate)
library(forcats)
#Reading in data
results <- read.csv("~/Documents/UAEPlacement/CodingChallenges/results.csv")

# Calculate home results
home_results <- results %>%
  mutate(
    win  = ifelse(home_score > away_score, 1, 0),
    draw = ifelse(home_score == away_score, 1, 0),
    loss = ifelse(home_score < away_score, 1, 0)
  ) %>%
  group_by(home_team) %>%
  summarise(
    wins = sum(win),
    draws = sum(draw),
    losses = sum(loss)
  ) %>%
  rename(team = home_team)

# Calculate away results
away_results <- results %>%
  mutate(
    win  = ifelse(away_score > home_score, 1, 0),
    draw = ifelse(away_score == home_score, 1, 0),
    loss = ifelse(away_score < home_score, 1, 0)
  ) %>%
  group_by(away_team) %>%
  summarise(
    wins = sum(win),
    draws = sum(draw),
    losses = sum(loss)
  ) %>%
  rename(team = away_team)

# Combine home and away stats
team_stats <- bind_rows(home_results, away_results) %>%
  group_by(team) %>%
  summarise(
    total_wins = sum(wins),
    total_draws = sum(draws),
    total_losses = sum(losses)
  ) %>%
  mutate(
    performance_score = total_wins + total_draws - total_losses
  ) %>%
  arrange(desc(performance_score))

# Take top 10 teams by performance
top10 <- team_stats %>%
  top_n(10, performance_score) %>%
  arrange(desc(performance_score))

# Convert to long format for grouped bar chart
top10_long <- top10 %>%
  select(team, total_wins, total_draws, total_losses) %>%
  pivot_longer(
    cols = c(total_wins, total_draws, total_losses),
    names_to = "result_type",
    values_to = "count"
  )

# Clean up labels
top10_long$result_type <- factor(top10_long$result_type,
                                 levels = c("total_wins", "total_draws", "total_losses"),
                                 labels = c("Wins", "Draws", "Losses"))

# Order teams by total_wins for plotting
top10_long <- top10_long %>%
  mutate(team = factor(team, levels = top10$team[order(top10$total_wins, decreasing = TRUE)]))

# Plot grouped bar chart (ordered by wins)
ggplot(top10_long, aes(x = team, y = count, fill = result_type)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9)) +
  geom_text(aes(label = count),
            position = position_dodge(width = 0.9),
            vjust = -0.3,
            size = 3) +
  labs(
    title = "Top 10 Teams by Number of Wins",
    x = "Team",
    y = "Number of Results",
    fill = "Result Type"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))


########################### Analyzing Dominant Teams by Era
# Step 2: Convert date to Date type and extract the year
results$date <- as.Date(results$date)
results$year <- year(results$date)

# Step 3: Create 20-year eras
results <- results %>%
  mutate(era = paste0(floor((year - 1870) / 20) * 20 + 1870, 
                      "-", 
                      floor((year - 1870) / 20) * 20 + 1889))

# Step 4: Compute wins per team per era
wins <- results %>%
  mutate(winner = case_when(
    home_score > away_score ~ home_team,
    away_score > home_score ~ away_team,
    TRUE ~ NA_character_
  )) %>%
  filter(!is.na(winner)) %>%
  group_by(era, winner) %>%
  summarise(total_wins = n(), .groups = "drop")

# Step 5: Get top 5 teams per era
top5_teams_per_era <- wins %>%
  group_by(era) %>%
  slice_max(total_wins, n = 5) %>%
  ungroup()

# Step 6: Plot the results
ggplot(top5_teams_per_era, aes(x = fct_reorder(winner, total_wins), 
                               y = total_wins, 
                               fill = winner)) +
  geom_col(show.legend = FALSE) +
  geom_text(aes(label = total_wins), vjust = -0.3, size = 3) +
  facet_wrap(~era, scales = "free_y") +
  coord_flip() +
  labs(
    title = "Top 5 Dominant Teams by 20-Year Era (Based on Wins)",
    x = "Team",
    y = "Number of Wins"
  ) +
  theme_minimal() +
  theme(
    axis.text.y = element_text(size = 8),
    strip.text = element_text(face = "bold", size = 10)
  )

