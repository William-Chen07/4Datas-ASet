print(RaceResults %>%
  ggplot(aes(x = TeamName, y = Points)) +
  geom_boxplot())

