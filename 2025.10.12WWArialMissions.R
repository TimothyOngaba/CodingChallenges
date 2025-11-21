'''
Core task; 
Did poor weather reduce the number of missions on a given day?
Were mission outcomes (success vs. failure, losses vs. survivals) correlated with weather factors?
Can you build a model that predicts the likelihood of a mission being flown (or its success) based on the weather? (OPTIONAL)
'''

#Loading Relevant packages
library(readr)
library(dplyr)

#Reading data in
weather_station_locations_in_ <- read_csv("UAEPlacement/CodingChallenges/weather_station_locations(in).csv")
weather_summary_in_ <- read_csv("UAEPlacement/CodingChallenges/weather_summary(in).csv", col_types = cols(Date = col_date(format = "%m/%d/%Y")))
aerial_operations_in_ <- read_csv("UAEPlacement/CodingChallenges/aerial_operations(in).csv", col_types = cols(`Mission Date` = col_date(format = "%m/%d/%Y"))) 
                                                            
#Merging weather with mission dates
aerial_operations_in_ <- aerial_operations_in_ %>%
  rename(Mission_Date = `Mission Date`)
MissionsFullSet <- aerial_operations_in_ %>%
  left_join(weather_summary_in_, by = c("Mission_Date" = "Date"), relationship = "many-to-many")

