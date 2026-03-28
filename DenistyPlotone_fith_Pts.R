print(RaceResults %>%
  ggplot(aes(x = (Points)^(1/5), fill = TeamName)) +
  geom_density(alpha = .3))