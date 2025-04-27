#install.packages("tidytuesdayR")
tuesdata <- tidytuesdayR::tt_load('2025-01-21')
''' Potential things to plot
Here are some potential topics to investigate using plots.
- What is the number of expedition members and success rate of different countries?
- The number of remaining peaks with year
- How has the success rate changed over time
- How has the use of Oxygen changed over time? '''

library(tidyverse)

# Filter relevant columns
exped_data <- tuesdata[["exped_tidy"]] %>%
  select(NATION, SUCCESS1, SUCCESS2, SUCCESS3, SUCCESS4)

# Convert to long format
success_long <- exped_data %>%
  pivot_longer(cols = starts_with("SUCCESS"), names_to = "Success_Stage", values_to = "Success") %>%
  filter(!is.na(NATION))

# Count expeditions per country
country_participants <- exped_data %>%
  filter(!is.na(NATION)) %>%
  count(NATION, name = "Participants")

# Calculate success rates
country_success_stage <- success_long %>%
  group_by(NATION, Success_Stage) %>%
  summarise(
    total = n(),
    successes = sum(Success == TRUE, na.rm = TRUE),
    success_rate = (successes / total) * 100,
    .groups = "drop"
  ) %>%
  left_join(country_participants, by = "NATION") %>%
  mutate(
    NATION_LABEL = paste0(NATION, " (", Participants, ")")
  )

# Plot , I frist plotted with ggplot so to have a comparison on for tidyplot
ggplot(country_success_stage, aes(x = fct_reorder(NATION_LABEL, -success_rate), y = success_rate, fill = Success_Stage)) +
  geom_col(position = position_dodge(width = 0.8)) +
  geom_text(aes(label = sprintf("%.1f%%", success_rate)), 
            position = position_dodge(width = 0.8), vjust = -0.5, size = 3) +
  labs(
    title = "Success Rates by Country and Success Stage",
    x = "Country (Participants)",
    y = "Success Rate (%)",
    fill = "Success Column"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1)))

#########################################

length(unique(exped_data$PEAKID))

# Get expedition data
exped_data <- tuesdata[["exped_tidy"]]

# Total unique peaks across all time
all_peaks <- unique(exped_data$PEAKID)
total_peaks <- length(all_peaks)

# Unique peaks climbed each year
peaks_per_year <- exped_data %>%
  filter(!is.na(YEAR), !is.na(PEAKID)) %>%
  group_by(YEAR) %>%
  summarise(climbed_peaks = n_distinct(PEAKID)) %>%
  mutate(remaining_peaks = total_peaks - climbed_peaks)

# Plot
ggplot(peaks_per_year, aes(x = YEAR, y = remaining_peaks)) +
  geom_col(fill = "steelblue") +
  geom_text(aes(label = remaining_peaks), vjust = -0.5, size = 3) +
  labs(
    title = "Number of Remaining Peaks by Year",
    x = "Year",
    y = "Remaining Unclimbed Peaks"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1)))

####################################
library(lubridate)
exped_data <- tuesdata[["exped_tidy"]]

# Convert SMTDATE to actual date format (if not already)
exped_data <- exped_data %>%
  mutate(SMTDATE = as.Date(SMTDATE))

# Count successful summits (non-NA SMTDATEs) per year
success_by_year <- exped_data %>%
  filter(!is.na(SMTDATE)) %>%
  count(YEAR, name = "successful_summits")

# Plot
ggplot(success_by_year, aes(x = YEAR, y = successful_summits)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_text(aes(label = successful_summits), vjust = -0.5, size = 3) +
  labs(title = "Summit Successes Over Time",
       x = "Year",
       y = "Number of Successful Summits") +
  theme_minimal()
##############################
exped_data <- tuesdata[["exped_tidy"]]

# Group by YEAR and SEASON_FACTOR and count oxygen usage
o2_use_by_year_season <- exped_data %>%
  filter(O2USED == TRUE) %>%
  group_by(YEAR, SEASON_FACTOR) %>%
  summarise(oxygen_used = n(), .groups = 'drop')

# Plot
ggplot(o2_use_by_year_season, aes(x = factor(YEAR), y = oxygen_used, fill = SEASON_FACTOR)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  geom_text(aes(label = oxygen_used), 
            position = position_dodge(width = 0.9), vjust = -0.5, size = 3) +
  labs(title = "Oxygen Use Over Time by Season",
       x = "Year",
       y = "Number of Expeditions Using Oxygen",
       fill = "Season") +
  theme_minimal()

# # install.packages("tidyplots")
# library(tidyplots)
# library(ggplot2)
# 
# # Make sure the data is in the right format for ggplot
# # Ensure the dataset has proper aggregated counts if needed
# o2_use_by_year_season_summary <- o2_use_by_year_season %>%
#   dplyr::group_by(YEAR, SEASON_FACTOR) %>%
#   dplyr::summarize(oxygen_used = sum(oxygen_used, na.rm = TRUE))
# 
# # Create the plot
# ggplot(o2_use_by_year_season_summary, aes(x = YEAR, y = oxygen_used, fill = SEASON_FACTOR)) +
#   geom_bar(stat = "identity") +
#   labs(
#     title = "Oxygen Use Over Time by Season (tidyplots)",
#     x = "Year",
#     y = "Number of Expeditions",
#     fill = "Season"
#   ) +
#   theme_minimal()

library(tidyplots)

library(tidyplots)

tidyplot(country_success_stage) %>%
  add_col(x = "NATION_LABEL", y = "success_rate", fill = "Success_Stage", position = "dodge") %>%
  add_text(aes(label = sprintf("%.1f%%", success_rate)), position = position_dodge(width = 0.8), vjust = -0.5, size = 3) %>%
  add_title("Success Rates by Country and Success Stage") %>%
  adjust_x_axis_title("Country (Participants)") %>%
  adjust_y_axis_title("Success Rate (%)") %>%
  adjust_legend_title("Success Column") %>%
  theme_tidyplot() %>%
  adjust_x_axis(angle = 45)









