if (!require(dplyr)) install.packages("dplyr")
if (!require(ggplot2)) install.packages("ggplot2")

library(dplyr)
library(ggplot2)
RaceResults <- read.csv("RaceResults.csv")
print(RaceResults %>%
  ggplot(aes(x = Points, fill = TeamName)) +
  geom_density(alpha = .3))