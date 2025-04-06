'''
What the common opening moves? By ranks?
How many turns does a game last based on player ranking?
What move patterns explain the game outcome?'''

#install.packages("tidyverse")
#Calling required packages
library(tidyverse)

#Reading in the data
Chessgames <- read.csv("~/Documents/UAEPlacement/Chessgames.csv")

# Filter for wins by mate and game opening moves
mate_openings <- Chessgames %>%
  filter(victory_status == "mate", !is.na(opening_name)) %>%
  mutate(opening_name = str_split(opening_name, pattern = ":")) %>% 
  unnest(opening_name) %>%
  mutate(opening_name = str_trim(opening_name)) %>%
  count(opening_name, sort = TRUE)

# View top 10 openings that led to mate
head(mate_openings, 10)

mate_openings %>% 
  slice_max(n, n = 10) %>%
  ggplot(aes(x = reorder(opening_name, n), y = n)) +
  geom_col(fill = "darkred") +
  coord_flip() +
  labs(x = "Opening Name", y = "Checkmate Count", 
       title = "Top 10 Openings Leading to Checkmate") +
  theme_minimal()
######################################
library(dplyr)
library(ggplot2)
library(forcats)

# Combine white and black ratings into a single data frame for ranking
player_ratings <- Chessgames %>%
  mutate(
    white_player = white_id,
    black_player = black_id,
    white_rating = as.numeric(white_rating),
    black_rating = as.numeric(black_rating)
  ) %>%
  select(id, white_player, black_player, white_rating, black_rating, turns)

# 1. Get average ratings for both white and black players
player_ratings_long <- player_ratings %>%
  gather(key = "player_type", value = "player_id", white_player, black_player) %>%
  gather(key = "rating_type", value = "rating", white_rating, black_rating) %>%
  filter(player_type == str_replace(rating_type, "_rating", "_player")) %>%
  group_by(player_id) %>%
  summarise(avg_rating = mean(rating, na.rm = TRUE)) %>%
  arrange(desc(avg_rating)) %>%
  mutate(player_rank = row_number())

# 2. Get the average number of turns for each player
player_turns <- player_ratings %>%
  gather(key = "player_type", value = "player_id", white_player, black_player) %>%
  group_by(player_id) %>%
  summarise(avg_turns = mean(turns, na.rm = TRUE)) %>%
  arrange(desc(avg_turns))

# 3. Merge the ranking and the turns
player_data <- left_join(player_turns, player_ratings_long, by = "player_id") %>%
  arrange(desc(avg_rating)) %>%
  mutate(player_label = paste(player_id, "(", round(avg_rating), ")", sep = ""))

# 4. Filter for top 10 players based on average rating
top_10_players <- player_data %>%
  top_n(10, avg_rating)

# 5. Plot the top 10 players with their average number of turns
ggplot(top_10_players, aes(x = avg_turns, y = fct_reorder(player_label, avg_turns))) +
  geom_col(fill = "steelblue") +
  geom_text(aes(label = round(avg_turns, 1)), hjust = -0.2, color = "black") +  # Add average turn values on top of bars
  theme_minimal() +
  labs(
    title = "Average Number of Turns by Top 10 Players Based on Rating",
    x = "Average Turns",
    y = "Player (Rating)"
  ) +
  theme(axis.text.y = element_text(size = 10))  # Adjust the y-axis label size for better readability


##########################################
#What move patterns explain the game outcome?'''
library(dplyr)
library(tidyr)
# Split the moves column into individual moves
Chessgames <- Chessgames %>%
  mutate(moves_list = strsplit(moves, " "))  # Splitting moves by space into a list

# Create binary features for some common opening moves
Chessgames <- Chessgames %>%
  mutate(
    move_e4 = sapply(moves_list, function(x) sum(x == "e4") > 0),   # 1 if e4 appears, 0 otherwise
    move_Nf3 = sapply(moves_list, function(x) sum(x == "Nf3") > 0),
    move_d4 = sapply(moves_list, function(x) sum(x == "d4") > 0),
    move_queen = sapply(moves_list, function(x) sum(grepl("Q", x)) > 0),  # Count moves with Queen
    move_Nc3 = sapply(moves_list, function(x) sum(x == "Nc3") > 0),
    move_e5 = sapply(moves_list, function(x) sum(x == "e5") > 0)
  )

# Check the result to verify
head(Chessgames)

library(randomForest)

# Transform the victory_status column to a factor (since it's categorical)
Chessgames$victory_status <- as.factor(Chessgames$victory_status)

# Train the random forest model
set.seed(123)  # Set seed for reproducibility
model_rf <- randomForest(victory_status ~ move_e4 + move_Nf3 + move_d4 + move_queen + move_Nc3 + move_e5,
                         data = Chessgames, 
                         importance = TRUE)

# Check the model summary
print(model_rf)
# Predict using the trained random forest model
predictions <- predict(model_rf, Chessgames)

# Create a confusion matrix
table(predictions, Chessgames$victory_status)

# Calculate accuracy
accuracy <- mean(predictions == Chessgames$victory_status)
print(paste("Accuracy: ", accuracy))

# Optionally, we can visualize feature importance
importance(model_rf)
varImpPlot(model_rf)

"""moving the queen was a more predictive move of the outcome than any other move on the chessboard
  This was followed by the pawn to D4, E4, Knight to f3, pawn to e5 and lastly night to c3
""""

