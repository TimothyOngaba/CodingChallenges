library(rjson)
data <- fromJSON("https://gist.githubusercontent.com/jorinvo/7f19ce95a9a842956358/raw/e319340c2f6691f9cc8d8cc57ed532b5093e3619/data.json")
json_data <- fromJSON(paste(readLines(data), collapse=""))

library(purrr)
library(tibble)
# Replace NULLs with NA in each sublist
json_cleaned <- map(json_data, ~map(.x, ~if (is.null(.x)) NA else .x))

# Convert cleaned sublists to tibbles, then bind into one dataframe
data_df <- map_dfr(json_cleaned, as_tibble)

library(dplyr)
# Select name and card columns, remove rows with NA
filtered_df <- data_df %>%
  select(name, creditcard) %>%
  filter(!is.na(name) & !is.na(creditcard))
 

# Create filename based on today's date
filename <- paste0(format(Sys.Date(), "%Y%m%d"), ".csv")

# Write to CSV
write.csv(filtered_df, file = filename, row.names = FALSE)